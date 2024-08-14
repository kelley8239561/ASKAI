"""
This module give the ability to the management of tasks

Function start

"""

import os
import time
import psutil
from multiprocessing import (
    Process,
    Manager,
)
import multiprocessing
import threading
from threading import (
    Thread,
)
from concurrent.futures import (
    ThreadPoolExecutor, 
    as_completed,
    wait,
)
from database import taskDBO
from task import (
    planTask,
)
# 任务列表，待开始todo，已开始doing，已完成done
taskListTodo = []
taskListDoing = []
taskListDone = []

# 行动列表
actionList = []

shareZone:dict


def main():
    global taskListTodo,shareZone
    # 开辟dataManager，用于进程间数据共享
    taskManager = Manager()
    
    # 1. 根据配置开辟进程执行actionList
    
    
    # 2. 主进程处理taskList
    # 初始化任务列表
    taskListInitial()
    # 开始执行任务
    # 有任务，而且没结束
    with ThreadPoolExecutor(max_workers = 3) as threadPool:
        # 管理ThreadPool开辟的线程
        futureThreadList = []
        # 判断是否退出
        while shareZone.get('sysQuit') != 0:
            # 没有任务则循环监听
            if taskListTodo.__len__() == 0:
                # 1秒可以进行配置
                time.sleep(1)
                print(os.getpid(),threading.current_thread().ident,'Checking tasks...')

                continue
            # 有任务抛给planTask
            else:
                # 执行任务
                task = taskListTodo[0]
                # 开启子线程
                futureThread = threadPool.submit(planTask.planMain,task)            
                futureThreadList.append(futureThread)
                # time.sleep(10)
                print(os.getpid(),threading.current_thread().ident,task.getParam('taskInstruction'),'is ready to start')
                # taskListTodo去除，修改标记并为taskListDoing增加
                taskListTodo = taskListTodo[1:]
                task.setParam('status',1)
                taskListDoing.append(task)
        '''
        # 获取结果（暂时未想好怎么用）
        for future in as_completed(futureThreadList):
            result = future.result()
            # 任务完成，做好标记
            print(os.getpid(),threading.current_thread().ident,result,'Task exit')
        '''        
            
            

def taskListInitial():
    '''
    _summary_
    # initial 3 lists:taskListTodo,taskListDoing,taskListDone
    '''
    global taskListTodo,taskListDoing,taskListDone
    # get work tasks from database
    print(os.getpid(),threading.current_thread().ident,'Task list initial')
    taskList = taskDBO.selectAll(taskDBO.createConnection('asset/tasks/Task.db'))
    # 根据任务状态status进行分开处理
    for task in taskList:
        if task.getParam('status') == 0:
            taskListTodo.append(task)
        elif task.getParam('status') == 1:
            taskListDoing.append(task)
        else:
            taskListDone.append(task)
    print(os.getpid(),threading.current_thread().ident,'Task list initial result:','to do:',taskListTodo.__len__(),'doing:',taskListDoing.__len__(),'done:',taskListDone.__len__())

def addTask():
    pass

def start(crossProcessDataZone):
    """
    _summary_
    Start the task manager manually
    
    """
    print(os.getpid(),threading.current_thread().ident,'Task manager start')
    # 同步信息
    global shareZone
    shareZone = crossProcessDataZone
    print(os.getpid(),threading.current_thread().ident,shareZone)

    main()
    print(os.getpid(),threading.current_thread().ident,'Task manager is stopped')
    print(os.getpid(),threading.current_thread().ident,shareZone)

# 暂时没用，keyboard和taskManager是两个进程，没想好如何解决控制问题
def quit():
    global shareZone
    # do sth to quit
    shareZone['sysQuit'] = 0
    print(os.getpid(),threading.current_thread().ident,'Send quit command to task manager.')

def autoStart():
    """
    _summary_
    Manage the auto run status of service manager
    """
    
    pass

def getTask():
    """
    _summary_
    Get the lastest task
    """





