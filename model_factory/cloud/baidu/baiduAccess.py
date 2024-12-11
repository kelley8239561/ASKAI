import inspect
import os
import sys
import json
import base64
import threading
import time
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus

import requests
timer = time.perf_counter

class BaiduAI():
    
    def getParams(self):
        caller_frame = inspect.currentframe().f_back
        caller_function = caller_frame.f_code.co_name
        print(os.getpid(),threading.current_thread().ident,'caller_function is:',caller_function)
        
        if caller_function == 'tts':
            #流式语音合成
            appId = ""
            cuid =  "lmyAwSj9uetXxjxhGls7Rs81GndCOUKI" # 
            apiKey = 'BpXFN5rGQefOWp7AkHCxQ40O' # apikey
            secretKey = '2LMhUhJBrha4FLd6Ot3nevKBQ8p4Fujh' # secretkey
            url = "http://tsn.baidu.com/text2audio" # 接口地址
            tokenUrl = "http://aip.baidubce.com/oauth/2.0/token" # 获取token的地址，后面accessToken需要
            scope= "audio_tts_post"  # 有scope表示有tts能力，没有请在网页里勾选，非常旧的应用可能没有
            accessToken = self.fetchToken(tokenUrl,apiKey,secretKey,scope) # token访问
            rate = 16000 # 采样率，固定值16000 or 8000
            devPID = 1537  # 1537 表示识别普通话，使用输入法模型。根据文档填写PID，选择语言及识别模型
            ctp = 1 # 客户端类型，默认是1
            lan = 'zh' # 中英混合模式，目前没有其他模式
            per = 2 # 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美 
            spd = 5 # 语速，取值0-15，默认为5中语速    
            pit = 5 # 音调，取值0-15，默认为5中语调 
            vol = 5 # 音量，取值0-9，默认为5中音量
            aue = 6 # 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
            formats = {3:'mp3',4:'pcm',5:'pcm',6:'wav'}
            format = formats[aue]# 文件后缀只支持{3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}格式
            
            return {
                "appId":appId,
                "cuid":cuid,
                "apiKey":apiKey,
                "secretKey":secretKey,
                "url":url,
                "tokenUrl":tokenUrl,
                "scope":scope,
                "accessToken":accessToken,
                "rate":rate,
                "format":format,
                "devPID":devPID,
                "ctp":ctp,
                "lan":lan,
                "per":per,
                "spd":spd,
                "pit":pit,
                "vol":vol,
                "aue":aue,
            }

        elif caller_function == 'asr':
            #语音识别
            appId = ""
            cuid =  "lmyAwSj9uetXxjxhGls7Rs81GndCOUKI" # 
            apiKey = 'BpXFN5rGQefOWp7AkHCxQ40O' # apikey
            secretKey = '2LMhUhJBrha4FLd6Ot3nevKBQ8p4Fujh' # secretkey
            url = "http://vop.baidu.com/server_api" # 接口地址
            tokenUrl = "http://aip.baidubce.com/oauth/2.0/token" # 获取token的地址，后面accessToken需要
            scope= "audio_voice_assistant_get"  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有
            accessToken = self.fetchToken(tokenUrl,apiKey,secretKey,scope) # token访问
            rate = 16000 # 采样率，固定值16000 or 8000
            format = 'pcm' # 文件后缀只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
            devPID = 1537  # 1537 表示识别普通话，使用输入法模型。根据文档填写PID，选择语言及识别模型
            return {
                "appId":appId,
                "cuid":cuid,
                "apiKey":apiKey,
                "secretKey":secretKey,
                "url":url,
                "tokenUrl":tokenUrl,
                "scope":scope,
                "accessToken":accessToken,
                "rate":rate,
                "format":format,
                "devPID":devPID
            }
        
        elif caller_function == 'chat':
            return

        else:
            return 0
        
    def fetchToken(self,tokenUrl,apiKey,secretKey,scope):
            
            """
            #REST API?
            class DemoError(Exception):
                pass
            params = {'grant_type': 'client_credentials',
                    'client_id': apiKey,
                    'client_secret': secretKey}
            postData = urlencode(params)
            postData = postData.encode( 'utf-8')
            req = Request(tokenUrl, postData)
            try:
                f = urlopen(req)
                resultStr = f.read()
            except URLError as err:
                print('token http response http code : ' + str(err.code))
                resultStr = err.read()
            resultStr =  resultStr.decode()
            result = json.loads(resultStr)
            print(result)
            if ('access_token' in result.keys() and 'scope' in result.keys()):
                if scope and (not scope in result['scope'].split(' ')):  # SCOPE = False 忽略检查
                    raise DemoError('scope is not correct')
                print('SUCCESS WITH TOKEN: %s  EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
                return result['access_token']
            else:
                raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')
            """
            
            #"""
            #url = "https://aip.baidubce.com/oauth/2.0/token?client_id=BpXFN5****CxQ40O&client_secret=2LMhUh****p4Fujh&grant_type=client_credentials"
            url = tokenUrl+"?"+"client_id="+apiKey+"&"+"client_secret="+secretKey+"&"+"grant_type=client_credentials"
            payload = json.dumps("")
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            response = requests.request("POST", url, headers=headers, data=payload)
            result = response.json()
            # print(os.getpid(),threading.current_thread().ident,"get access token response:",result,type(result))
            print(os.getpid(),threading.current_thread().ident,"get access token",result.get('access_token'))
            return result.get('access_token')
            #"""
            
    def asr(self,content):
        # 获取配置参数
        params = self.getParams()
        
        # 文件后缀只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
        format = params.get('format')

        cuid = params.get('cuid')
        # 采样率，固定值
        rate = params.get('rate')  
        # 模型类型，普通版 or 其他
        devPID = params.get('devPID')
        # 模型访问地址
        url = params.get('url')
        token = params.get('accessToken')
        speech = base64.b64encode(content)
        # coding=utf-8
        speech = str(speech, 'utf-8')
        lenth = len(content)
        print(os.getpid(),threading.current_thread().ident,"The Content lenth to ASR is:",lenth)
        
        postParams = {
            'dev_pid': devPID,
            'format': format,
            'rate': rate,
            'token': token,
            'cuid': cuid,
            'channel': 1,
            'speech': speech,
            'len': lenth
        }
        postData = json.dumps(postParams, sort_keys=False)
        # print post_data
        req = Request(url, postData.encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        try:
            begin = timer()
            f = urlopen(req)
            resultStr = f.read()
            print (os.getpid(),threading.current_thread().ident,"Request time cost %f" % (timer() - begin))
        except URLError as err:
            print(os.getpid(),threading.current_thread().ident,'asr http response http code : ' + str(err.code))
            resultStr = err.read()
        resultStr = str(resultStr, 'utf-8')
        print(os.getpid(),threading.current_thread().ident,"ASR response is:",resultStr)
        resultDic = json.loads(resultStr)["result"][0]
        return resultDic
    
    def tts(self,content):
        # coding=utf-8
        params = self.getParams()
        # 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
        # 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美 
        per = params.get('per')
        # 语速，取值0-15，默认为5中语速
        spd = params.get('spd')
        # 音调，取值0-15，默认为5中语调
        pit = params.get('pit')
        # 音量，取值0-9，默认为5中音量
        vol = params.get('vol')
        # 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
        aue = params.get('aue')
        # 下载文件格式
        format = params.get('format')
        # 接口地址
        url = params.get('url')
        
        # 客户端id
        cuid = params.get('cuid')
        # accesstoken
        token = params.get('accessToken')
        # 客户端类型
        ctp = params.get('ctp')
        # 语言
        lan = params.get('lan')
        
        #异常处理
        class DemoError(Exception):
            pass
        """
        # String payload
        #payload=f'tex={content}tok={token}&cuid={cuid}&ctp={ctp}&lan={lan}&spd={spd}&pit={pit}&vol={vol}&per={per}&aue={aue}'
        # dic payload
        content = quote_plus(content)
        payload = {
            'tex':content,
            'tok':token,
            'cuid':cuid,
            'ctp':ctp,
            'lan':lan,
            'spd':spd,
            'pit':pit,
            'vol':vol,
            'per':per,
            'aue':aue
        }
        
        #payload = urlencode(payload)
        print(payload,type(payload))
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        print('This is tts result: ', response.text)
        resultStr = response.json().get('tex')
        print(resultStr)
        
        save_file = 'asset/tts/'+ format +'s/'+time.strftime('%H%M%S',time.localtime())+'result.' + format
        with open(save_file, 'wb') as of:
            of.write(resultStr)
        """
        
        
        
        #"""
        tex = quote_plus(content)  # 此处content需要两次urlencode
        print(tex)
        postParams = {'tok': token, 'tex': tex, 'per': per, 'spd': spd, 'pit': pit, 'vol': vol, 'aue': aue, 'cuid': cuid,
                'lan': lan, 'ctp': ctp}  # lan ctp 固定参数
        #postData = json.dumps(postParams, sort_keys=False)
        postData = urlencode(postParams)

        req = Request(url, postData.encode('utf-8'))
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        has_error = False
        try:
            f = urlopen(req)
            resultStr = f.read()

            headers = dict((name.lower(), value) for name, value in f.headers.items())

            has_error = ('content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0)
        except  URLError as err:
            print('asr http response http code : ' + str(err.code))
            resultStr = err.read()
            has_error = True

        save_file = "asset/logs/error.txt" if has_error else 'asset/tts/'+ format +'s/'+time.strftime('%H%M%S',time.localtime())+'result.' + format
        with open(save_file, 'wb') as of:
            of.write(resultStr)
            print(type(resultStr))

        if has_error:
            resultStr = str(resultStr, 'utf-8')
            print("tts api  error:" + resultStr)

        print("result saved as :" + save_file)
        #"""
        return (resultStr,save_file)
    
    