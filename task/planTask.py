"""
_summary_



_function_



"""
import os
import threading
import time
from task import taskClass
from langchain_community.chat_models import ChatZhipuAI
from models.cloud.teleAI import teleAIAccess
from models.cloud.zhipuai import zhipuaiAccess
from models.cloud.baidu import baiduAccess
from models.cloud.zhipuai.zhipuaiAccess import Zhipuai
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler,BaseCallbackHandler
from langchain_core.callbacks.stdout import StdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.base import ConversationChain
from task.prompts import chatPrompts,taskPrompts
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import RetryWithErrorOutputParser,OutputFixingParser
from task.parser import taskParser

appListTodo = []
appListDoing = []
appListDone = []

def planMain(task:taskClass.OriginTask):
    # 1. Task Split任务分解
    # 1-1. model初始化
    splitModel=('Zhipuai','glm-4-0520')
    print(os.getpid(),threading.current_thread().ident,'Start task:',task.getParam('id'),task.getParam('taskInstruction'))
    # 1-2. 获取结果
    splitResult = taskSplit(task.getParam('taskInstruction'),splitModel)
    print(os.getpid(),threading.current_thread().ident,splitResult)
    
    # 1-3. 结果保存
    
    
    # 2. 
    
    # appListTodo.append(appListGenerating)
    
    
    return task.getParam('id'),True

def taskExtract():
    pass

def taskSplit(taskInstruction,model=('Zhipuai','glm-4-0520')):
    print(os.getpid(),threading.current_thread().ident,'Split start...')
    service = eval(model[0])()
    apiKey = service.getParams().get('apiKey')
    os.environ["ZHIPUAI_API_KEY"] = apiKey
    # llm
    llm = ChatZhipuAI(
        model=model[1],
        temperature=0.5,
        streaming=True,
        callback_manager=CallbackManager([StdOutCallbackHandler()]), # StdOutCallbackHandler()
    )
    # prompt
    prompt = taskPrompts.taskSplit
    # print(os.getpid(),threading.current_thread().ident,prompt)
    # parser
    outputParser = taskParser.appTaskListOutputParser # JSON parser
    fixingParser = OutputFixingParser.from_llm(parser=outputParser,llm=llm) # JSON parser with fixing
    RetryParser = RetryWithErrorOutputParser.from_llm(parser=outputParser,llm=llm) # JSON parser with retry
    
    # chain for split 工作流
    # taskSplitChain = prompt | llm | outputParser # normal JSON parser
    # taskSplitChainNoParser = prompt | llm # for Debug: No parser
    taskSplitChainFixing = prompt | llm | fixingParser # for Debug: fixing parser
    # taskSplitChainRetry = prompt | llm | RetryParser.parse_with_prompt() # for Debug: retry parser
    # print(os.getpid(),threading.current_thread().ident,taskParser.appTaskListOutputParser.get_format_instructions())
    '''
    # normal JSON parser
    splitResult = taskSplitChain.invoke(
        {
            'humanInfor':taskInstruction,
        }
    )
    '''
    '''
    # for Debug: No parser
    splitResultNoParser = taskSplitChainNoParser.invoke(
        {
            'humanInfor':taskInstruction, 
        }
    )
    '''
    # for Debug: fixing parser
    splitResultFixing = taskSplitChainFixing.invoke(
        {
            'humanInfor':taskInstruction, 
        }
    )
    '''
    # for Debug: retry parser
    splitResultRetry = taskSplitChainRetry.invoke(
        {
            'humanInfor':taskInstruction, 
        }
    )
    '''
    # return splitResult,splitResultNoParser,splitResultFixing
    return splitResultFixing

def actionGenerate():
    a = 1
    b = 2
    return a,b