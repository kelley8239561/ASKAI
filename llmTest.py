from models.cloud.teleAI import teleAIAccess
from models.cloud.zhipuai import zhipuaiAccess
from models.cloud.baidu import baiduAccess
from auto.devices import audio

"""
LLM连通和使用测试
"""

"""
#Test for TeleAI.chat()
content = '''
          你为什么不是一个AI助手呢？
          '''

def chat(content):
    teleservice = teleAIAccess.TeleAI()
    
    answer = teleservice.chat(content)
    print(answer)
    return

chat(content)
"""


"""
#Test for TeleAI.tts()
content = '''
    websockets 是一个用于在Python中构建WebSocket服务器和客户端的库，重点关注正确性、简单性、健壮性和性能。它建立在asyncio之上，提供了一个优雅的基于协程的API。
'''

def tts(content):
    teleservice = teleAIAccess.TeleAI()
    teleservice.tts(content)
    print('success')
    return

tts(content)
"""

"""
#Test for TeleAI.asr()
content = "asset/recordings/wavs/120654 All.wav"
#content = "asset/recordings/pcms/120654 All.pcm"

def asr(content):
    teleservice = teleAIAccess.TeleAI()
    teleservice.asr(content)
    print('success')
    return

print(asr(content))
"""

"""
#Test for Zhipuai.chat()
content = [
            {"role": "system", "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"},
            {"role": "user", "content": "我对太阳系的行星非常感兴趣，特别是土星。请提供关于土星的基本信息，包括其大小、组成、环系统和任何独特的天文现象。"},
        ]

def chat(content):
    zhipuservice = zhipuaiAccess.Zhipuai()
    for ms in zhipuservice.chat(content):
        print(ms.content,end="")
    return

chat(content)
#for choicedelta in chat(content):
#    print(choicedelta.content,end='')
"""

"""
# Test for BaiduAI.asr()
# 初始化baiduService
baiduService = baiduAccess.BaiduAI()

# pcm文件读入
filename = "asset/recordings/pcms/163306 All.pcm"
with open(filename,"rb") as f:
    content = f.read()
    print('file read success!')

print(baiduService.asr(content))

"""


"""
# Test for BaiduAI.tts()
# 初始化baiduService
baiduService = baiduAccess.BaiduAI()
# 初始化audioService
audioService = audio.AudioService()

content = '我终于成功了，能不能给我一个吻，可以不可以，我不想要别的，我只想要一个吻，一个大大的吻，可以让我开心的不得了的吻，欧哈哈欧哈哈，苦吃苦吃卡'
result = baiduService.tts(content)
audioService.playStream(result[0])
print(result[1])

"""



