from auto.devices import audio
from task import dialogTask
import sounddevice
import threading
import time
import keyboard
from models.cloud.baidu import baiduAccess

"""
#传入duration给到Stream
#录制一段音频
audioService = audio.AudioService()
#查看当前设备状态
#print(sounddevice.query_devices())
result = audioService.recStream(3000)
print(result.shape)
"""

"""
#录制一段音频
#使用rec()不限duration Stream
audioService = audio.AudioService()
#查看当前设备状态
#print(sounddevice.query_devices())
result = audioService.recStreamByDuration()
print(result.shape)

"""

"""
# 查看当前设备状态
#print(sounddevice.query_devices())
# 初始化audioService
audioService = audio.AudioService()
def stopRec():
    print("listen")
    global audioService
    task = dialogTask.AudioDialog(audioService=audioService)
    task.audioListenByButtonPress()
    print("Thread end in Test")
    return
keyBoardThread = threading.Thread(target=stopRec,args=())
keyBoardThread.start()
#keyboard.wait('ctrl')
time.sleep(0.1)
result = audioService.recStreamByRecStopCut()
print("Main end in Test")
keyBoardThread.join()

baiduService = baiduAccess.BaiduAI()
for r in result[0:-1]:
    print(baiduService.asr(b''.join(r)))

"""

"""
#Button按键测试
audioService = audio.AudioService()
task = dialogTask.AudioDialog(audioService=audioService)
task.dialogByButtonPress() 

"""

#"""
#测试对话 audioChat
# 初始化audioService
audioService = audio.AudioService()
audioDialogService = dialogTask.AudioDialog(audioService=audioService)
audioDialogService.audioChat()

#"""