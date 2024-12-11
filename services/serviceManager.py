"""
This module is the manager of all the service which can keep the assistant ongoing.
Execute he main logic of the service running.
"""
from ast import Lambda
import multiprocessing
import time
from conf import initial
import task
from task import keyboardService, textService, voiceService, screenRecordService
from multiprocessing import Process,Manager
from threading import Thread
import os,psutil,threading

import task.keyboardService
import serviceTest

# 服务列表
serviceList = ()

# 共享空间
shareZone:dict

def main():
    global serviceList
    # 引用进程间数据共享
    global shareZone
    # config放入共享空间
    shareZone['config'] = initial.myConfig.configData
    
    # 已经运行的服务进程和线程列表
    
    dataManager = Manager()
    serviceRunningList = dataManager.list([
        {
            'GROUP':0,
            'NAME':main,
            'process':psutil.Process().pid, # 进程id
            'threads':[{
                'name': 'main',
                'thread': threading.current_thread().ident, # 线程id
            }],
        },
    ])
    
    # 进程实例列表
    pList = []
    
    # 根据key名称获取runningList中的一行
    def getRunningListByKey(key):
        result = []
        for running in serviceRunningList:
            result.append(running.get(key))
        return result
    
    # 向runningList中进程为group的增加线程id
    def addThreadToRuningList(name,group,thread): 
        for running in serviceRunningList:
            # 找到process的GROUP
            if running.get('GROUP') == group:
                # 插入一条Thread记录到'Threads'
                running.get('threads').append(
                    {
                        'name':name,
                        'thread':thread,
                    }
                )
                break
        return
    
    # 根据GROUP和MAIN顺序，对serviceList进行排名
    def serviceListSortByGROUPAndMAIN():
        # print(serviceList)
        n = len(serviceList)
        # print(serviceList[0][1].get('MAIN'),type(serviceList[0][1].get('MAIN')))
        for i in range(n):
            for j in range(n-i-1):
                if int(serviceList[j][1].get('GROUP')) > int(serviceList[j+1][1].get('GROUP')):
                    serviceList[j], serviceList[j+1] = serviceList[j+1], serviceList[j]
                elif int(serviceList[j][1].get('GROUP')) == int(serviceList[j+1][1].get('GROUP')):
                    if not serviceList[j+1][1].get('MAIN'):
                        serviceList[j], serviceList[j+1] = serviceList[j+1], serviceList[j]
        # print(serviceList)
    
    # 启动顺序排序
    serviceListSortByGROUPAndMAIN()
    print(os.getpid(),'Sorted services are:',serviceList)
    # 暂存进程包含的服务线程
    subServicesToRun = []
    # 逐个启动进程
    for service in serviceList:
        # 进程是否存在,如果存在则在当前进程开辟线程执行，如果不存在则开辟进程
        print(os.getpid(),"Start process :",service[1].get('GROUP'))
        # 把同一组Service加入到List，便于后续调用和传给对应的子进程
        subServicesToRun.append(service)  
        # service中MAIN=True，则启动进程，并且把后面需要启动的线程信息也传递过去threadToRunList
        if service[1].get('MAIN'):
            print(os.getpid(),"Start service :",service[0])
            print(os.getpid(),"Target function is:",service[1].get('TARGET'))
            p = Process(target=eval(service[1].get('TARGET')),args=(shareZone,serviceRunningList,subServicesToRun),name=service[1].get('NAME'))
            # 将依赖于该进程启动的服务传入，清空暂存的列表，以便后用
            subServicesToRun = []
            # 修改运行状态
            serviceRunningList.append(
                {
                    'GROUP': service[1].get('GROUP'),
                    'process':p.pid,
                    'thread':[],
                }
            )
            p.start()
            pList.append(p)
            
    
    # for service in serviceList.items():
    #     print(os.getpid(),"In serviceManager.main()")
    #     # 键盘服务
    #     if service[0] == 'KEYBOARDLISTENSERVICE':
    #         if service[1].get('MODE') == 'p':
    #             print(os.getpid(),__name__,"Add new process")
    #             p = Process(target=keyboardService.main,args=(serviceDataShareZone,))
    #             p.start()
    #             processList.append(p)
    #         elif service[1].get('MODE') == 't':
    #             t = Thread(target=keyboardService.main)
    #             t.start()  
    #             threadList.append(t)
    #     # 录音服务
    #     elif service[0] == 'VOICELISTENSERVICE':
    #         if service[1].get('MODE') == 'p':
    #             print(os.getpid(),__name__,"Add new process")
    #             p = Process(target=keyboardService.main,args=(serviceDataShareZone,))
    #             p.start()
    #             processList.append(p)
    #         elif service[1].get('MODE') == 't':
    #             t = Thread(target=keyboardService.main)
    #             t.start()  
    #             threadList.append(t)
    #     # 语音输出服务
    #     elif service[0] == 'SPEAKERSERVICE':
    #         pass
    #     # 录屏服务
    #     elif service[0] == 'SCREENRECORDSERVICE':
    #         pass
    #     else:
    #         pass  
    
    # recycle processes
    for p in pList:
        print(os.getpid(),threading.current_thread().ident,'Main end',p.name)
        p.join()
    
def start(serviceConfig,crossProcessDataZone):
    """
    _summary_
    Start the service manager manually
    
    """
    print(os.getpid(),threading.current_thread().ident,'Service manager start...')
    global serviceList
    #获取要启动的service
    serviceList = list(serviceConfig.items())
    #print(os.getpid(),serviceList)
    # 初始化共享空间
    global shareZone
    shareZone = crossProcessDataZone
    main()
    print(os.getpid(),"Services have already closed")
    return

def autoService():
    """
    _summary_
    Manage the auto run status of service manager
    """
    pass




