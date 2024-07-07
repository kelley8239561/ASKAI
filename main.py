"""
Start the assistant
    
"""
from task import taskManager,serviceManager
from multiprocessing import Process
from conf import initial
import os,time,psutil

if __name__ == '__main__':
    # initial配置项
    initial.initial()
    serviceConfig = initial.myConfig.configData.get('mainServiceConfig')
    psutil.Process(os.getpid())
    print(os.getpid(),'Get servie configuration successfully!')
    print(os.getpid(),'The configuration is: ',serviceConfig)
    
    # 启动监听器
    serviceManager.start(__name__,serviceConfig)
    
    print(os.getpid(),"Assistant service over")
    # 启动任务管理器和任务线程
    #taskProcess = Process(target=taskManager.start)
    #taskProcess.start()
    #taskProcess.join()


