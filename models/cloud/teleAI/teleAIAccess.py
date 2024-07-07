import uuid
import time
import requests
import hashlib
import json
import pdb
import time
import hashlib
import uuid
import websocket
import base64
import wave
import json
import inspect,psutil

class TeleAI():
    #获取appId，apiKey，secretKey，url，sessionId 
    def getParams(self):
        caller_frame = inspect.currentframe().f_back
        caller_function = caller_frame.f_code.co_name
        
        print(caller_function)
        
        if caller_function == 'tts':
            #流式语音合成
            appId = "F14B7F67075B4569B6B4395E4DFB446A"
            apiKey = "20F2E43BB96446A89003A99BA24BCC27"
            secretKey = "FCC466C163FF4599A330794F628DD245"
            url = "wss://150.223.245.42/csrobot/cschannels/openapi/ws/tts"
            return {
                "appId":appId,
                "apiKey":apiKey,
                "secretKey":secretKey,
                "url":url
            }

        elif caller_function == 'asr':
            #实时语音识别
            appId = "C5A5B21B19AF4EE29A5D83504D8E4665"
            apiKey = "C5A5B21B19AF4EE29A5D83504D8E4665"
            secretKey = "75C0B07AAC044904847B16D8F2DBFBAA"
            url = "wss://150.223.245.42/csrobot/cschannels/openapi/ws/asr"
            return {
                "appId":appId,
                "apiKey":apiKey,
                "secretKey":secretKey,
                "url":url
            }
        elif caller_function == 'chat':
            #12b插件辅助对话
            appId = "46287812AD574462833BF37CBF9C9997"
            apiKey = "46A286DF5A3E420C9E1F1669FE21ADCE"
            secretKey = "D2701FAA7F704B3FB13A98A3A558D850"
            url = "https://150.223.245.42/csrobot/cschannels/openapi/chat/bizDialog?apiKey=46A286DF5A3E420C9E1F1669FE21ADCE"
            return {
                "appId":appId,
                "apiKey":apiKey,
                "secretKey":secretKey,
                "url":url,
                "sessionId":self.sessionId
            }
        else:
            return 0
    
    #session
    sessionId = uuid.uuid4()
       
    def __init__(self):
        
        pass
    
    #更新sessionId
    def sessionIdRefresh(self):
        self.sessionId = uuid.uuid4()
        return
       
    #base64编码转换成WAV文件
    def base64_to_wav(self,data):
        # 解码Base64字符串
        audio_data = base64.b64decode(data)
        # 打开WAV文件写入器
        path = 'asset/tts/wavs/'
        filename = 'Demo voice.wav'
        with wave.open(path+filename, 'wb') as wf:
            # 设置WAV文件的参数，这里需要知道音频的具体参数（采样率、通道数、位深度等）
            nchannels = 1  # 单声道为1，立体声为2
            sampwidth = 2  # 每个样本的字节数，通常为1（8位）或2（16位）
            framerate = 16000  # 采样率，通常为44100Hz
            nframes = len(audio_data) // (nchannels * sampwidth)  # 计算总帧数
            comptype = "NONE"  # 压缩类型，如果是未压缩则为"NONE"
            compname = "not compressed"  # 压缩名称
            # 设置WAV文件头信息
            wf.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
            # 写入数据
            wf.writeframes(audio_data)
        print('语音合成文件以生成：' + filename)
        return

    #WAV文件转换成base64编码
    def wav_to_base64(self,filename):
        with wave.open(filename, 'rb') as wav_file:
            wav_data = wav_file.readframes(wav_file.getnframes())
            base64_data = base64.b64encode(wav_data)
            return base64_data.decode('utf-8')
    
    #签名需要SHA256加密
    def sha256_hash(self,message):
        # 创建SHA-256对象
        sha256 = hashlib.sha256()

        # 更新哈希对象的内容
        sha256.update(message.encode('utf-8'))

        # 计算哈希值
        hash_value = sha256.hexdigest()

        return hash_value

    #TTS接口
    def tts(self,content):
        #获取appId，apiKey，secretKey，url，sessionId
        params = self.getParams()
        
        #获取时间戳
        timestamp = str(int(time.time()))
        #traceId随机生成
        traceId = str(uuid.uuid4())
        apisign = self.sha256_hash(params.get("apiKey") + '-' + params.get("secretKey") + '-' + traceId + '-' + timestamp)
        url = (params.get("url") + "?apiKey="
                + params.get("apiKey") + "&appSign=" + apisign + "&traceId=" + traceId + "&timestamp=" + timestamp)
        print(url)
        # time.sleep(600)
        # 创建一个websocket连接
        ws = websocket.create_connection(url)
        # 从服务器接收消息
        response = ws.recv()
        print("Received message:", json.loads(response)["data"])
        # 发送开始识别消息到服务器
        #req_id实际使用时需要替换为随机值，text为需要合成语音的文字
        ws.send(json.dumps({"req_id": str(uuid.uuid4()), "text": content}))
        print("需要语音合成的文字Message sent")
        # 从服务器接收消息
        response2 = ws.recv()
        print("Received message:", json.loads(response2)["status_msg"])
        # 发送语音文件到服务器
        try:
            # 循环接收流式数据
            voice = ""
            while True:
                # 接收数据
                result = ws.recv()
                if result:
                    #返回的⾳频数据需要拼接起来再转为语音
                    voice = voice + json.loads(result)["result"]["audio"]
                else:
                    break
                #is_end=True代表合成结束
                if json.loads(result)["result"]["is_end"]:
                    #将拼接好的base64码转换为wav语音文件
                    self.base64_to_wav(voice)
                    break
        except Exception as e:
            print(e)
        finally:
            # 关闭连接
            ws.close()
            print("关闭成功")
        return

    #ASR接口
    def asr(self,content):
        #获取appId，apiKey，secretKey，url，sessionId
        params = self.getParams()
        
        #获取时间戳
        timestamp = str(int(time.time()))
        #traceId随机生成
        traceId = str(uuid.uuid4())
        #拼接apisign，并进行加密
        apisign = self.sha256_hash(params.get("apiKey") + '-' + params.get("secretKey") + '-' + traceId + '-' + timestamp)
        #拼接url
        ws_url = (params.get('url') + "?apiKey="
                + params.get("apiKey") + "&appSign=" + apisign + "&traceId=" + traceId + "&timestamp=" + timestamp)
        print(ws_url)
        # time.sleep(600)
        # 创建一个websocket连接
        ws = websocket.create_connection(ws_url)
        # 从服务器接收消息
        response = ws.recv()
        print("Received message:", json.loads(response)['data'])
        # 发送开始识别消息到服务器
        #req_id实际使用时需要替换为随机值
        ws.send(json.dumps({"req_id": str(uuid.uuid4()), "rec_status": 0}))
        print("开始识别Message sent")
        # 从服务器接收消息
        response2 = ws.recv()
        print("Received message:", json.loads(response2)["message"])
        # 发送语音文件到服务器
        #demo使用固定文件，实际使用需要传输实时pcm
        wav_base64_string = self.wav_to_base64(content)
        voice = json.dumps({"audio_stream": wav_base64_string, "rec_status": 1})
        ws.send(voice)
        print("语音编码Message sent")
        try:
            # 循环接收流式数据
            while True:
                # 接收数据
                print(0)
                result = ws.recv()
                print(1)
                if result:
                    print(2)
                    #返回的识别信息用后返回text中的信息覆盖之前返回的
                    voice = json.loads(result)["data"]["results"][0]["text"]
                    print(voice)
                else:
                    break
                #res_status=3代表识别结束
                if json.loads(result)["res_status"] >= 3:
                    print(3)
                    voice = json.loads(result)["data"]["results"][0]["text"]
                    print("识别最终结果：" + voice)
                    break
        except Exception as e:
            print('exception')
            print(e)
        finally:
            # 发送结束调用传输到服务器
            ws.send(json.dumps({"rec_status": 2}))
            print("结束调用Message sent")
            response3 = ws.recv()
            print("Received message:", json.loads(response3)["message"])
            # 关闭连接
            ws.close()
            print("关闭成功")
        return voice
    
    #聊天接口
    def chat(self,content):
        #获取appId，apiKey，secretKey，url，sessionId
        params = self.getParams()
        #获取时间戳
        timestamp = str(int(time.time()))
        #traceId随机生成
        traceId = str(uuid.uuid4())
        # 待加密内容
        sign_str = f"{params.get('apiKey')}-{params.get('secretKey')}-{traceId}-{timestamp}"
        '''
        #for Test
        print(params.get('apiKey'))
        print(params.get('secretKey'))
        print(traceId)
        print(timestamp)
        print(sign_str)
        '''
        # 签名
        sign = self.sha256_hash(sign_str)
        #sign = hashlib.sha256(sign_str.encode('utf-8')).hexdigest()
        # 构造请求头
        headers = {
            "App-Sign": sign,
            "Content-Type": "application/json;UTF-8"
        }
        # 构造请求体
        data = {
            "traceId": str(traceId),
            "timestamp": timestamp,
            "stream": False,
            "content": content,
            "sessionId": str(self.sessionId),
            "showPluginResult": False
        }
        # 发送POST请求
        response = requests.post(params.get("url"), headers=headers, json=data)
        #pdb.set_trace()
        # # 打印原始响应内容
        #print(response.content)
        # # 处理SSE响应
        # if response.status_code == 200:
        #     current_event = ""
        #     for line in response.iter_lines():
        #         print(line)
        # else:
        #     print(f"请求失败，状态码：{response.status_code}")
        # print(current_event)

        return response.content.decode("utf-8")

    


