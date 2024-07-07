"""
_summary_
Functions about the keyboard.

_funcs_

"""
import os,psutil
import time
import keyboard
from keyboard import KeyboardEvent
from task import dialogTask
import threading
from threading import Thread
import serviceTest


keyboardQuitFlag = True

# 共享空间引用
localShareZone:dict



def main(shareZone,serviceRunningList,subServicesToRun):
    """
    # keyboardService main function
    # param
        - shareZone: To share data from other process
        - serviceRunningList: The current state of the services
        - threadToRunList: service configuration to run in this main
    """ 
    global keyboardQuitFlag,localShareZone
    # 共享空间引用
    localShareZone = shareZone
    
    threadList = []
    tList = []
    
    # 子服务启动（service[1].get('MAIN') = False）
    for service in subServicesToRun[:-1]:
        if not service[1].get('MAIN'):
            print(os.getpid(),'Start sub service',service[0])
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
    
    # keyboard主服务
    print(os.getpid(),"Start keyboard mark")
    print(os.getpid(),"The keyboard listen tid is :",threading.current_thread().ident)
    
    '''
    # Test for multiprocessing.Manager() 操作特性
    print(os.getpid(),shareZone)
    tempShareZone = shareZone['dialogMark']
    tempShareZone['instructionMark'].append('111')
    print(os.getpid(),'修改完成：',tempShareZone)
    shareZone['dialogMark'] = tempShareZone
    print(os.getpid(),shareZone)
    '''
    
    # ctrl+a处理语音指令
    keyboard.add_hotkey(hotkey='ctrl+a',callback=dialogTask.AudioDialog.dialogMarkInstructionBegin,args=(time.time(),)) # 开始拾音
    keyboard.on_release_key(key='a',callback=dialogTask.AudioDialog.dialogMarkInstructionEnd) # 结束拾音
    #keyboard.add_hotkey(hotkey=,callback=)
    
    
    
    # 退出
    keyboard.add_hotkey('ctrl+esc',callback=keyboardQuit)
    while keyboardQuitFlag:
        time.sleep(0.5)
    print(os.getpid(),'Quit successfully')
    # 测试是否成功记录，并且写入共享内存
    print(os.getpid(),"The dialog record mark is")
    print(os.getpid(),shareZone)
    
    # 多线程结束合并
    for thread in tList:
        thread.join()
    
    return
    
def keyboardQuit():
    global keyboardQuitFlag,localShareZone
    print(os.getpid(),"Quit from the keyboard command")
    keyboard.unhook_all()
    keyboardQuitFlag = False
    # 将中止指令传给其他服务：1、音频录制服务listenMain，2、
    temp = localShareZone['dialogMark']
    temp['listenMark'] = keyboardQuitFlag
    localShareZone['dialogMark'] = temp

def keyboardClick(button):
    """
    _summary_
    To handle the keyboard event.
    """
    #print(os.getpid(),"The keyboard action is ", button.name,button.event_type,button.scan_code)
    return









