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


def audioToText(data:numpy.ndarray):
    print(os.getpid(),threading.current_thread().ident,'ASR Begin')
    targetModel = ('BaiduAI','asr')
    service = eval(targetModel[0])()
    
    result = eval('service.'+targetModel[1])(b''.join(data))
    # print(os.getpid(),threading.current_thread().ident,result)
    return result

def textToAudio(data:str,model= ('BaiduAI','tts')):
    service = eval(model[0])()
    # tts获取bytes并写入文件(bytes,fileurl)
    result = eval('service.'+model[1])(data)
    print(os.getpid(),threading.currentThread().ident,'Text to Audio:',data,'is completed.')
    # result = (bytes,fileurl)
    return result

# 图像结构化
def imageStructurize(data):
    pass

def textEmbedding(data):
    pass

def imageEmbedding(data):
    pass

