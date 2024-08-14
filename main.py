"""
Start the assistant
    
"""
import threading
from task import taskManager,serviceManager
from multiprocessing import Manager, Process
from conf import initial
import os,time,psutil

crossProcessDataZone:dict

if __name__ == '__main__':
    # initial配置项
    initial.initial()
    # 进程池
    mainProcessList = []
    
    # task和service间共享空间
    manager = Manager()
    crossProcessDataZone = manager.dict({
        # 对话记录，Mark标记
        'dialogMark' : { 
            'instructionMark':[], # 语音指令接收标记
            'listenMark':True, # Test的退出标记后续需要挪出
        },
        # 大模型对话的问题
        'userInstructions' : [],
        # 需要进行语音的文字,list of str
        'readyToAudio' : [],
        # 需要进行播放的audio，list of ndarray
        'readyToSpeech': [],
        # 任务列表taskListTodo,taskListDoing,taskListDone
        'taskListTodo': [],
        'taskListDoing': [],
        'taskListDone': [],
        # 应用列表appListTodo,appListDoing,appListDone
        'appListTodo': [],
        'appListDoing': [],
        'appListDone': [],
        # 动作列表actionListTodo,actionListDoing,actionListDone
        'actionListTodo': [],
        'actionListDoing': [],
        'actionListDone': [],
        # Configuration
        'config': {},
        # 系统退出
        'sysQuit':1
    })
    
    
    print(os.getpid(),threading.current_thread().ident,'1111',crossProcessDataZone)
    # TaskManager启动
    taskProcess = Process(target=taskManager.start,args=(crossProcessDataZone,))
    taskProcess.start()
    mainProcessList.append(taskProcess)
    
    # ServiceManager启动
    serviceConfig = initial.myConfig.configData.get('mainServiceConfig')
    print(os.getpid(),threading.current_thread().ident,'Get servie configuration successfully!')
    print(os.getpid(),threading.current_thread().ident,'The configuration is: ',serviceConfig)
    serviceManager.start(serviceConfig,crossProcessDataZone)
    
    for process in mainProcessList:
        process.join()
    
    print(os.getpid(),threading.current_thread().ident,"Assistant service over")
    


