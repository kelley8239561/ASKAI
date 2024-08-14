import os
import threading
import time
import models
from models.cloud.teleAI import teleAIAccess
from models.cloud.zhipuai import zhipuaiAccess
from models.cloud.baidu import baiduAccess
from auto.devices import audio
import keyboard,psutil
from task import keyboardService
from models.cloud.zhipuai.zhipuaiAccess import Zhipuai
import langchain
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.callbacks import StdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.base import ConversationChain
from task.parser import taskParser
from task.prompts import chatPrompts,taskPrompts
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import OutputFixingParser,RetryWithErrorOutputParser

#定义监听的按键为'space'空格键
buttonName = 'ctrl'
#按住空格只监听一次
listenState = 1
instructionMarkState = 1
# Mark标记
dialogMark = {
    'instructionMark':[]
}

def simpleChat(userMessage,model=('Zhipuai','glm-4-flash'),):
    service = eval(model[0])()
    apiKey = service.getParams().get('apiKey')
    os.environ["ZHIPUAI_API_KEY"] = apiKey
    llmForChat = ChatZhipuAI(
        model=model[1],
        temperature=0.5,
        streaming=True,
        callback_manager=CallbackManager([StdOutCallbackHandler()]),
    )
    promptForChat = chatPrompts.simpleChatPrompt
    outputParserForChat = StrOutputParser()
    # fixingParser = OutputFixingParser(parser=outputParserForChat).from_llm(llm=llmForChat,parser=outputParserForChat)
    chatChain = promptForChat | llmForChat | outputParserForChat
    return chatChain.stream(
        {
            'humanInfor':userMessage,
        }
    )
        
    
    
    
    '''
    conversation = ConversationChain(
        llm=llmForChat,
        verbose=True,
        memory=ConversationBufferMemory()
    )
    
    conversation.predict()
    '''
    
    # llmForChat.invoke(message)
    
    '''
    for response in chat.stream(message):
        # print(response.content,end='')
        yield response.content
    '''

class AudioDialog():
    """
    For Audio Dialog Use
    """
    # 初始化audioService类，用于录音和音频播放
    audioService:audio.AudioService
    # 初始化TeleAI类，用于调用ASR和TTS接口
    teleService:teleAIAccess.TeleAI
    # 初始化zhipuAI类，用于调用LLM
    zhipuService:zhipuaiAccess.Zhipuai
    # 初始化BaiduAI类，用于调用LLM
    baiduService:baiduAccess.BaiduAI
    
    def __init__(
                self,
                audioService:audio.AudioService,
                teleService = teleAIAccess.TeleAI(),
                zhipuService = zhipuaiAccess.Zhipuai(),
                baiduService = baiduAccess.BaiduAI()
                 ):
        self.audioService = audioService
        self.teleService = teleService
        self.zhipuService = zhipuService
        self.baiduService = baiduService
        return    

    def audioListenByButtonPress(self):
        """
            # Control the audio service by button press
            ## When the buttonStart is down, push the start message to the audio service 
            ## When the setting button @buttonName is op, push the stop message to the audio service
            ## The method of pushing message is to change the value of streamStop, streamStart and streamQuit
        """
        #监听button，有press返回true，否则返回false
        def buttonListen(button):
            #print("callback:hook")
            global buttonName
            global listenState
            if button.name == buttonName and button.event_type == 'down' and listenState == 1:
                #关闭按键监听
                listenState = 0
                print("Start")
                #重置结束符，并且开始录音
                setattr(self.audioService,'streamStop',False)
                setattr(self.audioService,'streamStart',True)
                print("setting over")
            
            if button.name == buttonName and button.event_type == 'up':
                #打开按键监听
                listenState = 1
                print("end")
                #重置开始符，并且结束录音
                setattr(self.audioService,'streamStart',False)
                setattr(self.audioService,'streamStop',True)
        
        print("listen to keyboard")        
        keyboard.hook(callback=buttonListen)
        print("ready")
        #退出录音
        keyboard.wait('esc')
        #关闭流
        setattr(self.audioService,'streamQuit',True)
        
        return
    
    def audioListenByButtonControl(self,buttonStart,startAction,buttonStop,stopAction,buttonQuit,quitAction):
        """
            # Control the audio service by button press
            ## When the buttonStart is down, push the start message to the audio service 
            ## When the setting button @buttonName is op, push the stop message to the audio service
            ## The method of pushing message is to change the value of streamStop, streamStart and streamQuit
        """
        #监听button，有press返回true，否则返回false
        def buttonListen(button):
            #print("callback:hook")
            global buttonName
            global listenState
            if button.name == buttonName and button.event_type == 'down' and listenState == 1:
                #关闭按键监听
                listenState = 0
                print("Start")
                #重置结束符，并且开始录音
                setattr(self.audioService,'streamStop',False)
                setattr(self.audioService,'streamStart',True)
                print("setting over")
            
            if button.name == buttonName and button.event_type == 'up':
                #打开按键监听
                listenState = 1
                print("end")
                #重置开始符，并且结束录音
                setattr(self.audioService,'streamStart',False)
                setattr(self.audioService,'streamStop',True)
        
        print("listen to keyboard")        
        keyboard.hook(callback=buttonListen)
        print("ready")
        #退出录音
        keyboard.wait('esc')
        #关闭流
        setattr(self.audioService,'streamQuit',True)
        
        return

    def audioChat(self):
        """
            This is the core function to chat with LLM by audio
            # 1. Press button 'ctrl' to start record audios waves and stop when button 'ctrl' is on
            # 2. Pass the record audio waves to ASR and get text result
            # 3. Use the text result as prompt to chat with LLM
            # 4. Get the answer from LLM and parse it to waves(by TTS), and play it.
        """
        
        
        # 监听键盘事件，做录音控制，单独用keyBoardThread做监听
        def stopRec():
            print("listen")
            self.audioListenByButtonPress()
            print("Thread end in Test")
            return
        keyBoardThread = threading.Thread(target=stopRec,args=())
        keyBoardThread.start()
        #keyboard.wait('ctrl')
        # 为什么这里不停止，线程会卡住
        time.sleep(0.2)
        
        # 获取listen数据流
        recResult = self.audioService.recStreamByRecStopCut()
        print("Main end in Test",recResult.__len__)
        keyBoardThread.join()

        # ASR
        asrResult = ''
        for r in recResult[0:-1]:
            asrResult = asrResult + self.baiduService.asr(b''.join(r))
        print(asrResult)    
        
        # LLM
        content = [
            {"role": "system", "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"},
            {"role": "user", "content": asrResult},
        ]
        tempResult = ''
        for ms in self.zhipuService.chat(content):
            chatResultList = []
            tempResult += ms.content
            print(ms.content,end="")
            #if ms.content.endswith((',','.','?','!','，','。','？','！')):
            #    # TTS
            #    chatResultList.append(tempResult)
            #    tempResult = ''
        
        self.audioService.playStream(self.baiduService.tts(tempResult))
        
    @staticmethod
    def dialogMarkInstructionBegin(timeStamp):
        global instructionMarkState,dialogMark
        if instructionMarkState == 1:
            instructionMarkState = 0
            print(os.getpid(),'Record Begin: ',timeStamp)
            mark = {
                'begin':timeStamp,
                'end':0
            }
            # 拿出要修改的dict的一级路径
            tempShareZone = keyboardService.localShareZone['dialogMark']
            tempShareZone['instructionMark'].append(mark)
            keyboardService.localShareZone['dialogMark'] = tempShareZone
            #dialogMark['instructionMark'].append(mark) #单元测试用，未加入到进程间共享数据
        
    @staticmethod
    def dialogMarkInstructionEnd(button):
        global instructionMarkState,dialogMark
        if instructionMarkState == 0:
            print(os.getpid(),'Record end: ',button.time)
            tempShareZone = keyboardService.localShareZone['dialogMark']
            tempShareZone['instructionMark'][-1]['end'] = button.time
            keyboardService.localShareZone['dialogMark'] = tempShareZone
            #dialogMark['instructionMark'][-1]['end'] = button.time # For Test，未加入到进程间共享数据
            instructionMarkState = 1
        

            
            
        

        
        
        
    