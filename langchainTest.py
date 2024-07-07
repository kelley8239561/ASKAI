from task import dialogTask
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

#"""
# Test for dialogTask.chat
'''
# message for AI, System and Human
message = [
    AIMessage(content="Hi."),
    SystemMessage(content="Your role is a poet."),
    HumanMessage(content="Write a short poem about AI in four lines."),
]
'''
message = "你知道我叫什么名字么？如果知道请回答"
for result in dialogTask.simpleChat(message):
    print(result,end='')
#"""