"""
_summary_
All the service about the text are here

_function_
main #

"""
# 共享空间引用
import asyncio
from datetime import date
import os
from threading import Thread
import threading
import time
from task import basicTask,dialogTask

from conf import initial
from auto.file import file

# 进程通信空间引用
localShareZone:dict

def textMain(shareZone,serviceRunningList,subServicesToRun,):
    # 共享空间引用
    global localShareZone
    localShareZone = shareZone
    
    threadList = []
    tList = []
    # 子服务启动（service[1].get('MAIN') = False，按照排序，最后一个 = True）
    for service in subServicesToRun[:-1]:
        # if not service[1].get('MAIN'):
        print(os.getpid(),threading.currentThread().ident,'Start sub service',service[0])
        print(os.getpid(),threading.currentThread().ident,service[1].get('TARGET'))
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
    
    print(os.getpid(),'Start text operation')
    # 0 获取配置列表
    # 暂时没有
    
    # 1 启动协程处理所有Text相关任务事件
    asyncio.run(textOperation())
    
    # 4 退出
    print(os.getpid(),threading.currentThread().ident,'End text operation')
    
    for thread in tList:
        thread.join()
    
async def textOperation():
    instructionTask = asyncio.create_task(instructionToAudio())
    responseTask = asyncio.create_task(responseToInstruction())
    testTask = asyncio.create_task(test())
    print(os.getpid(),threading.currentThread().ident,'Start async text operation')
    await asyncio.gather(instructionTask,responseTask,testTask)
    print(os.getpid(),threading.currentThread().ident,'End async text operation')

async def instructionToAudio():
    # 引用共享空间地址
    global localShareZone
    # stream的最小粒度
    streamLenth = 10
    model = ('BaiduAI','tts')
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
            await asyncio.sleep(streamLenth/5)
            continue
        # 文字转音频
        else:
            # assert localShareZone.get('readyToAudio').__len__() == 0
            for instruction in localShareZone.get('readyToAudio'):
                readyToSpeechList = []
                while len(instruction) != 0:
                    textSlice = instruction[0:streamLenth]
                    result = basicTask.textToAudio(textSlice,model)
                    # 加入分段（streamLenth个字）
                    readyToSpeechList.append(result)
                    
                    # 每次完成后，截断text为没有的部分
                    instruction = instruction[streamLenth:]
                # 写入到进程共享空间
                print(os.getpid(),threading.currentThread().ident,type(readyToSpeechList[0]),readyToSpeechList[0].__len__())
                readyToSpeechList = localShareZone.get('readyToSpeech') + readyToSpeechList
                localShareZone['readyToSpeech'] = readyToSpeechList
                # print(os.getpid(),threading.currentThread().ident,type(localShareZone['readyToSpeech'][0]),localShareZone['readyToSpeech'][0].__len__())
                print(os.getpid(),threading.currentThread().ident,instruction,'to audio is completed')
                    
            # 共享空间移除已经完成的instruction
            readyToAudioList = localShareZone.get('readyToAudio')[1:]
            print(os.getpid(),threading.currentThread().ident,'The updated readyToAudio is:',readyToAudioList,)
            localShareZone['readyToAudio'] = readyToAudioList       
    
    print(os.getpid(),threading.currentThread().ident,'End Text to Audio')
    return

async def responseToInstruction():
    # For Debug
    print(os.getpid(),threading.currentThread().ident,'Start response to instructions')
    # 引用共享空间地址
    global localShareZone
    # stream的最小粒度
    streamLenth = 30
    model=('Zhipuai','glm-4-flash')
    while True:
        print(os.getpid(),threading.currentThread().ident,time.time(),localShareZone.get('userInstructions'))
        # 判断是否有停止命令
        if not localShareZone['dialogMark']['listenMark']:
            break
        # 延长步长到streamLenth/5，每秒5字，跟下面播放一致
        # userInstructions没有可以转音频
        if localShareZone.get('userInstructions').__len__() == 0:
            await asyncio.sleep(streamLenth/5)
            continue
        # 文字转音频
        else:
            # assert localShareZone.get('userInstructions').__len__() == 0
            for instruction in localShareZone.get('userInstructions'):
                # 暂时接收结果的变量
                tempResult = ''
                for resultSlice in dialogTask.simpleChat(instruction,model):
                    tempResult = tempResult + resultSlice
                    # 超出一段的字数限制，做切分
                    if resultSlice.__len__() >= streamLenth:
                        # 引用共享区并存储
                        readyToAudioList = localShareZone.get('readyToAudio')
                        readyToAudioList.append(tempResult)
                        localShareZone['readyToAudio'] = readyToAudioList
                        # 写入日志文件
                        with open(file.getPath('llmLog'),'a') as llmLogFile:
                            llmLogFile.write(os.getpid(),threading.currentThread().ident,time.time(),tempResult)
                        
                        print(os.getpid(),threading.currentThread().ident,'Write',tempResult,'to the share zone')

                        # 清空暂时接收结果的变量
                        tempResult = '' 
                
                # 处理最后剩余的字符串字符串
                # 引用共享区并存储
                readyToAudioList = localShareZone.get('readyToAudio')
                readyToAudioList.append(tempResult)
                localShareZone['readyToAudio'] = readyToAudioList
                # 写入日志文件
                with open(file.getPath('llmLog'),'a') as llmLogFile:
                    llmLogFile.write(str(os.getpid())+str(threading.currentThread().ident)+str(time.time())+tempResult)
                print(os.getpid(),threading.currentThread().ident,'Write',tempResult,'to the share zone') 
                # 结束一个instruction
                print(os.getpid(),threading.currentThread().ident,'Response over:',instruction)
                # 共享空间移除已经完成的instruction
                userInstructionsList = localShareZone.get('userInstructions')[1:]
                print(os.getpid(),threading.currentThread().ident,'The updated userInstructions is:',userInstructionsList,)
                localShareZone['userInstructions'] = userInstructionsList       
    
    # 结束
    print(os.getpid(),threading.currentThread().ident,'End Text to Audio')
    
    
    
    return

async def test():
    print(os.getpid(),threading.currentThread().ident,'Test start when Instrcion To Audio work')
    while True:
        # 判断是否停止
        if not localShareZone['dialogMark']['listenMark']:
            break
        print(os.getpid(),threading.currentThread().ident,'Test asyncio test in loop')
        await asyncio.sleep(2)
    print(os.getpid(),threading.currentThread().ident,'Test end when Instrcion To Audio work')
