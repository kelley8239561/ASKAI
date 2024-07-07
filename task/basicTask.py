"""
_summary_
All the basic Tasks are here 

_functions_
audioRecognization  # ASR

"""
import os
import threading
import numpy
from models.cloud.baidu.baiduAccess import BaiduAI

async def audioRecognization(data:numpy.ndarray):
    print(os.getpid(),threading.current_thread().ident,'ASR Begin')
    targetModel = ('BaiduAI','asr')
    service = eval(targetModel[0])()
    
    result = eval('service.'+targetModel[1])(b''.join(data))
    # print(os.getpid(),threading.current_thread().ident,result)
    return result

async def textToAudio(data:str):
    
    return