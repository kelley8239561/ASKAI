from task import dialogTask
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from task import planTask

"""
# Test for dialogTask.chat
'''
# message for AI, System and Human
message = [
    AIMessage(content="Hi."),
    SystemMessage(content="Your role is a poet."),
    HumanMessage(content="Write a short poem about AI in four lines."),
]
'''
message = "给老板发送一封邮件"
for result in dialogTask.simpleChat(message):
    print(result,end='')
"""

#"""
# Test for planTask.taskSplit()
taskInstruction = "预约明天下午3点的会议"

splitResult = planTask.taskSplit(taskInstruction=taskInstruction)
print(type(splitResult),splitResult)
# print("normal....................")
# print(type(splitResult[0]),splitResult[0])
# print("original....................")
# print(type(splitResult[1]),splitResult[1])
# print("fixing....................")
# print(type(splitResult[2]),splitResult[2])
# print("retry....................")
# print(type(splitResult[3]),splitResult[3])
#"""