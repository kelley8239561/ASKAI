import os
import time
import wave,psutil
import soundfile
from PIL import Image

path = {
    'recordWaves':'asset/recordings/wavs/',
    'recordPcms':'asset/recordings/pcms/',
    'ttsWaves':'asset/tts/wavs/',
    'ttsPcms':'asset/tts/pcms/',
    'errorLog':'asset/logs/error.txt',
    'llmLog' : 'asset/logs/chat.txt',
    'screenShot':'asse,t/recordings/pics/screenShot'
}

def getPath(task):
    global path
    return path[task]

# audio 转成 wav文件并保存
def audioStreamToWav(data,task,filename,samplerate,channels,sampwidth):
    """
    #通过soundfile.write()方式
    path = 'asset/recordings/wavs/'
    filename = filename+'.wav'
    soundfile.write(path+filename,data,self.__samplerate)
    print('Write result to ' + path + filename)
    """
    
    # 通过wave.open()方式
    filePath = getPath(task)
    filename = filename+'.wav'
    # 转为二进制
    audioData = b''.join(data)
    with wave.open(filePath+filename,'wb') as wavFile:
        # 设置WAV文件的参数，这里需要知道音频的具体参数（采样率、通道数、位深度等）
        nchannels = channels  # 单声道为1，立体声为2
        sampwidth = sampwidth  # 每个样本的字节数，通常为1（8位）或2（16位）
        framerate = samplerate  # 采样率，通常为44100Hz
        nframes = len(audioData) // (nchannels * sampwidth)  # 计算总帧数
        comptype = "NONE"  # 压缩类型，如果是未压缩则为"NONE"
        compname = "not compressed"  # 压缩名称
        # 设置WAV文件头信息
        wavFile.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
        # 写入数据
        wavFile.writeframes(audioData)
    print(os.getpid(),'Write result to ' + filePath + filename)
   
# audio 转成 pcm文件并保存 
def audioStreamToPCM(data,task,filename,samplerate,channels,sampwidth,comptype = "NONE",compname = "not compressed"):
    filePath = getPath(task)
    filename = filename+'.pcm'
    audioData = b''.join(data)
    with wave.open(filePath+filename,'wb') as pcmFile:
        # 设置WAV文件的参数，这里需要知道音频的具体参数（采样率、通道数、位深度等）
        nchannels = channels  # 单声道为1，立体声为2
        sampwidth = sampwidth  # 每个样本的字节数，通常为1（8位）或2（16位）
        framerate = samplerate  # 采样率，通常为44100Hz
        nframes = len(audioData) // (nchannels * sampwidth)  # 计算总帧数
        comptype = comptype  # 压缩类型，如果是未压缩则为"NONE"
        compname = compname  # 压缩名称
        # 设置WAV文件头信息
        pcmFile.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
        pcmFile.writeframes(audioData)
    print(os.getpid(),'Write result to ' + filePath + filename)

# image 存储未png图像
def picSave(image,fileName=str(time.time())+'.png'):
    if isinstance(image,Image.Image):
        image.save(getPath('screenShot')+fileName)


 
# for Test 清空文件列表 
def emptyDir(urls):
    for url in urls:
        print(url)
        for file in os.listdir(url):
            print(file)
            if os.path.isfile(url+file):
                pass
                # os.remove(url+file)

        