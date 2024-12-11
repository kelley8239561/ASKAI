"""
_summary_
Task defination

"""

class OriginTask():
    id: int # id
    name:str # 名称
    status: int # 状态，0未开始，1已开始，2已结束
    taskInstruction: str # 任务信息，文本+图像
    objective: str # 目标信息，文本+图像
    appTaskList = [] # 子任务
    
    def __init__(self,tupleData:tuple):
        self.id = tupleData[0]
        self.name = tupleData[1]
        self.status = tupleData[2]
        self.taskInstruction = tupleData[3]
        self.objective = tupleData[4]
        pass
    
    def setParam(self,param,value):
        exec(f"self.{param} = {value}")
        return
    
    
    def getParam(self,param):
        return eval('self.'+param)

class AppTask():
    id: int # id
    name:str # 名称
    status: int # 状态，0未开始，1已开始，2已结束
    app: str # app or api 名称
    taskInstruction: str # 任务信息，文本+图像
    objective: str # 目标信息，文本+图像
    actionTaskList = [] # 子任务
    
    def __init__(self,tupleData:tuple):
        self.id = tupleData[0]
        self.name = tupleData[1]
        self.status = tupleData[2]
        self.app = tupleData[3]
        self.taskInstruction = tupleData[4]
        self.objective = tupleData[5]
        pass
    
    def setParam(self,param,value):
        exec(f"self.{param} = {value}")
        return
    
    
    def getParam(self,param):
        return eval('self.'+param)

 