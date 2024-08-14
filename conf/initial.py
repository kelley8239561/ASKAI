"""
_summary_
    - Read the initial environment settings when start.

_class_
    - config # save the configs in memory
        - load() -> dict
        - getConfig(*args) -> list

_functions_:
    - initial() -> dict
    
"""


import os,psutil
import yaml

class config:
    configData:dict
    def __init__(self,configInitial={}):
        self.configData = configInitial
    
    # 从文件中读取YAML配置
    def load(self,urls):
        for url in urls:
            with open(url, 'r',encoding='utf-8') as file:
                self.configData[url.split('/')[-1].split('.')[0]] = yaml.safe_load(file)

# 临时变量存储
myConfig = config()

def initial():
    # 初始化配置
    global myConfig
    urls = [
        'conf/mainServiceConfig.yaml',
        'conf/voiceListenServiceConfig.yaml',
        'conf/screenRecordServiceConfig.yaml'
    ]
    # config文件路径
    
    myConfig.load(urls)
    print(os.getpid(),'Successfully loading config files')
    print(myConfig.configData)