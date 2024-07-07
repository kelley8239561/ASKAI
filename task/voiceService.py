
import threading
import os,time,psutil,numpy,asyncio
import task
from threading import Thread
from auto.devices.audio import AudioService
from conf import initial
from auto.file import file
from task import basicTask
from models.cloud.baidu.baiduAccess import BaiduAI

# 共享空间引用
localShareZone:dict


def listenMain(shareZone,serviceRunningList,subServicesToRun,):
    # 共享空间引用
    global localShareZone
    localShareZone = shareZone
    
    threadList = []
    tList = []
    # 子服务启动（service[1].get('MAIN') = False）
    for service in subServicesToRun[:-1]:
        # if not service[1].get('MAIN'):
        print(os.getpid(),'Start sub service',service[0])
        print(service[1].get('TARGET'))
        t = Thread(target=eval(service[1].get('TARGET')),name=service[1].get('NAME'))
        t.start()
        tList.append(t)
        threadList.append(
            {
                'name':service[1].get('NAME'),
                'thread':t.ident,
            }
        )
    # 更新serviceRunningList
    for i in range(serviceRunningList.__len__()):
        if subServicesToRun[0][1].get('GROUP') == serviceRunningList[i].get('GROUP'):
            temp = serviceRunningList[i]
            temp['threads']= threadList
            serviceRunningList[i] = temp
    
    print(os.getpid(),'Start listen')
    print(os.getpid(),shareZone)
    # 0 获取配置列表
    myConfig = initial.config()
    # print(subServicesToRun[-1]) # for Test
    print(os.getpid(),'The url is:',subServicesToRun[-1][1].get('CONFIG')[0])
    myConfig.load([subServicesToRun[-1][1].get('CONFIG')[0]])
    
    print(os.getpid(),myConfig.configData)
    recordConfig = myConfig.configData.get(subServicesToRun[-1][1].get('CONFIG')[0].split('/')[-1].split('.')[0]).get(subServicesToRun[-1][1].get('CONFIG')[1])
    print(os.getpid(),recordConfig)
    
    # 1 启动监听服务，循环获取stream数据
    # 1-1 基础信息初始化
    samplerate = recordConfig.get('samplerate')
    channels = recordConfig.get('channels')
    dtype = recordConfig.get('dtype')
    sampwidth = recordConfig.get('sampwidth')
    audioBufferLenth = recordConfig.get('audioBufferLenth') # audioBuffer的长度（s） 
    stepLenth = recordConfig.get('stepLenth') # 记录的步长，最小计时为0.5s，即每0.5秒返回一次音频流数据
    
    # 暂存的音频流(nympy ndarray)
    audioStreamCount = 0 # 接收Stream的次数
    audioBufferCount = 0
    audioBuffer = numpy.empty((0,channels),dtype=dtype) # 暂存一段开始录音后的音频
    instructionMark = [] # 记录提问Mark点
    instructionBuffer = numpy.empty((0,channels),dtype=dtype) # 提问录音音频
    
    # audio实例初始化
    audioService = AudioService(
        samplerate = samplerate,
        channels = channels,
        dtype = dtype, 
    )
    # 1-1 获取流并放入buffer中
    for audioData in audioService.recStream(stepLenth):
        audioStreamCount  = audioStreamCount + 1 # 记录次数+1
        # for Test
        # print(os.getpid(),'audioCount',audioBufferLenth/stepLenth*audioBufferCount+audioStreamCount) # for Test
        # print(os.getpid(),'audioBuffer',audioBuffer.shape) # for Test
        # print(os.getpid(),'instructionBuffer',instructionBuffer.shape) # for Test
        # 2 判断是否退出
        if not shareZone['dialogMark']['listenMark']:
            # 2-1 通知音频流关闭
            audioService.streamQuit = True
        # print(os.getpid(),audioData[0].shape)
        # print(os.getpid(),audioData[1].shape)
        audioBuffer = numpy.concatenate((audioBuffer,audioData),axis=0)
        # 3 判断Mark没有更新，如果更新则截取对应的音频流
        # 3-1 长度一致，可能是没有对话，也可能是对话没有结束
        if shareZone['dialogMark']['instructionMark'].__len__() == instructionMark.__len__():
            # 没有提问（instruction），一直做Record
            if shareZone['dialogMark']['instructionMark'].__len__() == 0:
                if audioStreamCount*stepLenth >= audioBufferLenth:
                    # 写入文件
                    file.audioStreamToWav(
                        audioBuffer,
                        task = 'recordWaves',
                        filename = 'Record' + str(audioBufferCount) + ' at ' + str(time.time()),
                        samplerate = samplerate,
                        channels = channels,
                        sampwidth = sampwidth,
                    )
                    
                    # audioBuffer清零，streamCount（接收流的数量）清零，写入文件的数量+1
                    audioBufferCount = audioBufferCount + 1
                    audioStreamCount = 0
                    audioBuffer = numpy.empty((0,channels),dtype=dtype)
            # 有提问（instruction），要同时做记录，并且做问题抽取
            else:
                # 3-1-1 没有新对话
                if (shareZone['dialogMark']['instructionMark'][-1]['end'] != 0) and (instructionMark[-1]['end'] != 0):
                    # 3-1-1-1 audioBufferLenth超过设定，则写入文件，并重置
                    if audioStreamCount*stepLenth >= audioBufferLenth:
                        # 写入文件
                        file.audioStreamToWav(
                            audioBuffer,
                            task = 'recordWaves',
                            filename = 'Record' + str(audioBufferCount) + ' at ' + str(time.time()),
                            samplerate = samplerate,
                            channels = channels,
                            sampwidth = sampwidth,
                        )
                        
                        # audioBuffer清零
                        audioBufferCount = audioBufferCount + 1
                        audioStreamCount = 0
                        audioBuffer = numpy.empty((0,channels),dtype=dtype)
                # 3-1-2 有新对话没结束，也不是这次结束的
                elif (shareZone['dialogMark']['instructionMark'][-1]['end'] == 0) and (instructionMark[-1]['end'] == 0):
                    
                    pass
                
                # 3-1-3 有新对话没结束，但是本次结束了
                elif (shareZone['dialogMark']['instructionMark'][-1]['end'] != 0) and (instructionMark[-1]['end']==0):
                    instructionMark[-1]['end'] = audioBuffer.shape[0]
                    instructionBuffer = numpy.empty((0,channels),dtype=dtype)
                    instructionBuffer = audioBuffer[instructionMark[-1]['begin']:instructionMark[-1]['end']]
                    instructionText = asyncio.run(basicTask.audioRecognization(instructionBuffer))
                    # 更新共享区，将instructionText写入
                    textList = localShareZone.get('readyToAudio')
                    textList.append([instructionText,])
                    localShareZone['readyToAudio'] = textList
                    print(os.getpid(),threading.current_thread().ident,'Instruction over, the instruction text is:',localShareZone['readyToAudio'][-1])
                    file.audioStreamToWav(
                        instructionBuffer,
                        task = 'recordWaves',
                        filename = 'Instruction' + str(instructionMark.__len__()) + ' at ' + str(time.time()),
                        samplerate = samplerate,
                        channels = channels,
                        sampwidth = sampwidth,
                    )
                           
                else:
                    print(os.getpid(),'error, this situation will never exist')
                
        # 3-1 长度不一致，Mark有更新，shareZone['dialogMark']['instructionMark'] > instructionMark.__len__()
        else:
            # 补齐Mark
            
            instructionMark.append(
                {
                    'audioBufferCount':audioBufferCount,
                    'begin':audioBuffer.shape[0],
                    'end':0,
                }
            )
            # 判断输入是否结束，用shareZone['dialogMark']['instructionMark'][-1][end]是否为0判断
            
    # 4 音频流断流，尾部做保存
    if audioBuffer.shape[0] != 0:
        file.audioStreamToWav(
            audioBuffer,
            task = 'recordWaves',
            filename = 'Record' + str(audioBufferCount) + ' at ' + str(time.time()),
            samplerate = samplerate,
            channels = channels,
            sampwidth = sampwidth,
        )
    
    print(os.getpid(),'Listen Result:')
    print(os.getpid(),'Totle stream:',audioStreamCount)    
    print(os.getpid(),'Totle instruction:',instructionMark.__len__())         
        
    # 3-1-1 共享共建存储
    # 3-1-2 文件读写
    # 3-2 定期存取音频
    # 4 退出
    
    '''
    while True:
        if not shareZone['dialogMark']['listenMark']:
            break
        time.sleep(1)
    '''
    print(os.getpid(),'End listen')
    print(os.getpid(),'Mark result is:')
    print(os.getpid(),shareZone) 
    
    for thread in tList:
        thread.join()
    
    return

def speechMain():
    # 进程间共享空间地址引用
    global localShareZone
    
    print(os.getpid(),'Start speech')
    # 同时开启textToAudio和audioToSpeech
    asyncio.run(speech())
    # print(os.getpid(),threading.currentThread().ident,localShareZone.get('dialogMark'))
    print(os.getpid(),threading.currentThread().ident,'End speech')
    return

async def speech():
    audioToSpeechTask = asyncio.create_task(audioToSpeech())
    textToAudioTask = asyncio.create_task(textToAudio())
    print(os.getpid(),threading.currentThread().ident,'Start async speech')
    await asyncio.gather(textToAudioTask,audioToSpeechTask)
    print(os.getpid(),threading.currentThread().ident,'End async speech')

async def audioToSpeech():
    # For Test
    print(os.getpid(),threading.currentThread().ident,'In audioToSpeech')
    # 进程间共享空间地址引用
    global localShareZone
    # audio操作实例
    audioService = AudioService()
    
    # stream的最小粒度
    streamLenth = 10
    
    # 循环粒度（判断退出以及最小播放）
    while True:
        # For Test
        print(os.getpid(),threading.currentThread().ident,time.time(),'Ready to speech number is:',localShareZone.get('readyToSpeech').__len__())
        # 判断是否有停止命令
        if not localShareZone['dialogMark']['listenMark']:
            break
        # 延长步长到streamLenth/5，每秒5字，跟下面播放一致
        if localShareZone.get('readyToSpeech').__len__() == 0:
            time.sleep(streamLenth/5)
            continue
        # 是否有要说的话，如果有，流式
        while localShareZone.get('readyToSpeech').__len__() != 0:
            print(os.getpid(),threading.currentThread().ident,'In')
            # 播放分段
            audioService.playStream(localShareZone.get('readyToSpeech')[0][0])
            # 共享空间移除已经完成的speech
            readyToSpeechList = localShareZone.get('readyToSpeech')[1:]
            localShareZone['readyToSpeech'] = readyToSpeechList
            # 删除暂存文件（for debug）
            os.remove('asset/tts/wavs/'+localShareZone.get('readyToSpeech')[0][1]) 

async def textToAudio():
    # 引用共享空间地址
    global localShareZone
    # stream的最小粒度
    streamLenth = 10
    model = ('BaiduAI','tts')
    # 初始化模型服务
    service = eval(model[0])()
    print(os.getpid(),threading.currentThread().ident,'Start Text to Audio')
    
    while True:
        print(os.getpid(),threading.currentThread().ident,time.time(),localShareZone.get('readyToAudio'))
        # 判断是否有停止命令
        if not localShareZone['dialogMark']['listenMark']:
            break
        # 延长步长到streamLenth/5，每秒5字，跟下面播放一致
        # readyToAudio没有可以转音频 or readyToSpeech >10 已经超过10条还未播放
        # print(os.getpid(),threading.currentThread().ident,'The readyToAudio')
        if localShareZone.get('readyToAudio').__len__() == 0 or localShareZone.get('readyToSpeech').__len__() >= 10:
            time.sleep(streamLenth/5)
            continue
        # 文字转音频
        else:
            # assert localShareZone.get('readyToAudio').__len__() == 0
            for instruction in localShareZone.get('readyToAudio'):
                for text in instruction:
                    
                    while len(text) != 0:
                        textSlice = text[0:streamLenth]
                        # tts获取bytes并写入文件
                        result = eval('service.'+model[1])(textSlice)
                        readyToSpeechList = localShareZone.get('readyToSpeech')
                        readyToSpeechList.append(result)
                        localShareZone['readyToSpeech'] = readyToSpeechList
                        
                        # 每次完成后，截断text为没有的部分
                        text = text[streamLenth:]
                    print(os.getpid(),threading.currentThread().ident,instruction,'to text is completed')
                    
            # 共享空间移除已经完成的instruction
            readyToAudioList = localShareZone.get('readyToAudio')[1:]
            print(os.getpid(),threading.currentThread().ident,'The updated readyToAudio is:',readyToAudioList,)
            localShareZone['readyToAudio'] = readyToAudioList       
    
    print(os.getpid(),threading.currentThread().ident,'End Text to Audio')

def listen():
    pass