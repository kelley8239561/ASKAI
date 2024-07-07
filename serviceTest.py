import os,threading,psutil
import time
from task import keyboardService
import task
import task.keyboardService

def mainTest():
    print(os.getpid(),threading.current_thread().ident,'In Test Service')
    while True:
        if not keyboardService.localShareZone['dialogMark']['listenMark']:
            break
        time.sleep(1)
    print(os.getpid(),'Do something for Test')
    print(os.getpid(),'End Test Servie')
    
def screenRecord(serviceDataShareZone,serviceRunningList,subServicesToRun):
    print(os.getpid(),'In screen record Service')
    while True:
        if not serviceDataShareZone['dialogMark']['listenMark']:
            break
        time.sleep(1)
    print(os.getpid(),'Do the screen analysis')
    print(os.getpid(),'End screen record Servie')
    