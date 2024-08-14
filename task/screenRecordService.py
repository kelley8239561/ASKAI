"""
_summary_
Screen Record and save as Videos

_function_


"""

import asyncio
import datetime
import os
from threading import Thread
import threading
import time
from PIL import ImageGrab
import numpy
import cv2


# 进程通信空间引用
localShareZone:dict

def screenRecordMain(shareZone,serviceRunningList,subServicesToRun,):
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
    
    asyncio.run(screenRecord())
    
    # 4 退出
    print(os.getpid(),threading.currentThread().ident,'End text operation')
    
    for thread in tList:
        thread.join()


async def screenRecord():
    # 初始化config
    myConfig = localShareZone.get('config').get('screenRecordServiceConfig').get('SCREENRECORD')
    print(os.getpid(),threading.current_thread().ident,"The configuration is",myConfig)
    
    fps = myConfig.get('fps')  # 帧率
    saveURL = myConfig.get('saveURL') # 保存文件夹
    fileURL = getVideoPath(saveURL) # 文件名
    # 视频写入对象
    video = cv2.VideoWriter(fileURL, cv2.VideoWriter_fourcc(*'XVID'), fps,
                                     ImageGrab.grab().size)
    print(os.getpid(),threading.current_thread().ident,"Start screen record")
    # 时间标记，用于保存多个文件
    flag = 0
    audioLenth = myConfig.get('audioLenth')
    # 这里可以优化循环的事件，以提升视频帧率
    # time1 = 0.0
    # time2 = 0.0
    # time3 = 0.0
    # time4 = 0.0
    # time5 = 0.0
    while True:
        # time1 = time.time()
        flag = flag + 1
        # 超过audioLenth，自然截断视频
        if flag > audioLenth:
            print(os.getpid(),threading.current_thread().ident,"Save video:",fileURL)
            fileURL = getVideoPath(saveURL)
            video = cv2.VideoWriter(fileURL, cv2.VideoWriter_fourcc(*'XVID'), fps,
                                     ImageGrab.grab().size)
            flag = 0
        # 1、获取截图
        rawImage = ImageGrab.grab()
        # time2 = time.time()
        cv2Image = cv2.cvtColor(numpy.array(rawImage), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
        # time3 = time.time()
        # 2、写入文件
        saveToAudio(video,cv2Image)
        # time4 = time.time()
        # 4、结束
        if not ifRecording():
            break
        # time5 = time.time()
        # print(os.getpid(),flag,'cost....',time2-time1,time3-time2,time4-time3,time5-time4)
    # print(os.getpid(),threading.current_thread().ident,time.time()-startTime,flag,flag/(time.time()-startTime))
    video.release()
    cv2.destroyAllWindows()
    print(os.getpid(),threading.current_thread().ident,"End screen record")


def saveToAudio(video:cv2.VideoWriter,image):
    # print(os.getpid(),threading.current_thread().ident,flag,'Video writing begin')
    video.write(image)
    # print(os.getpid(),threading.current_thread().ident,flag,'Video writing end')
    return

def getVideoPath(saveURL):
    # 录屏保存的文件目录路径
    if not os.path.exists(saveURL):
        os.makedirs(saveURL)
    # 得到录屏保存的文件路径 按照时间创建文件夹
    fileName = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '_screen.avi'
    # 文件路径
    fileURL = os.path.join(saveURL, fileName)
    return fileURL

def ifRecording():
    # 读取共享空间中的停止符
    return localShareZone['dialogMark']['listenMark']



    