from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain_core.pydantic_v1 import BaseModel, Field


# app task parser
class AppTask(BaseModel):
    app: str = Field(description='完成任务要使用的app/页面名称')# app or api 名称
    task: str = Field(description='在当前app或页面需要完成的任务描述')# 任务信息，文本+图像
    objective: str = Field(description='在当前app或页面完成任务后需要达到的状态')# 目标信息，文本+图像

class AppTaskList(BaseModel):
    taskInstruction:str = Field(escription='要完成的任务描述')
    tasks:list[AppTask] = Field(description='完成taskInstruction需要的AppTask列表，每一行是一个AppTask')

appTaskListOutputParser = PydanticOutputParser(pydantic_object=AppTaskList)
# 查看输出解析器的内容，会被输出成json格式
# print(appTaskListOutputParser.get_format_instructions())