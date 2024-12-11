import time
from zhipuai import ZhipuAI
import inspect,psutil


class Zhipuai():
    
    def __init__(self) -> None:
        pass
    
    #获取必要参数，api_key,url
    def getParams(self):
        return {
            "apiKey":"3e045dc364024e449bc1bb5b7b2e4680.cWky13ALQM2YyqZ6",
            "url":"https://open.bigmodel.cn/api/paas/v4/chat/completions"
        }

    #model调用是否合法，合法True，不合法False
    def modelCheck(modelname):
        #zhipuai官网上有效模型名及对应可能调用的方法
        modellist = {'glm-4-0520':['chat'],
                     'glm-4':['chat'],
                     'glm-4-air':['chat'],
                     'glm-4-airx':['chat'],
                     'glm-4-flash':['chat'],
                     'glm-4v':['chat'],
                     'glm-3-turbo':['chat'],
                     'cogview-3':['chat'],
                     'charglm-3':['chat'],
                     'emohaa':['chat'],
                     'embedding-2':[],
                     }
        if modelname in list(modellist.keys()):
            caller_function = inspect.currentframe().f_back.f_code.co_name
            if caller_function in modellist[modelname]:
                return True
            else:
                return False
        else:
            return False
    
    def chat(self,content,stream=True,modelname='glm-4-flash'):
        params = self.getParams()
        
        #建立连接实例
        client = ZhipuAI(api_key=params.get('apiKey'))
        response = client.chat.completions.create(
            model=modelname,
            messages=content,
            stream=True,
        )
        
        #处理结果，返回一个list
        message = []
        for chunk in response:
            delta = chunk.choices[0].delta
            message.append(delta)
            yield(delta)
            #print(chunk.choices[0].delta)
            
        #return message
    
