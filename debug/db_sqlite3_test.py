#-----------------------------
# Test for do_operations.initial() and create_table
import sys
sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
from capacities.basic.db import operation_db
from logs import logging_operation
from realtime_chat import main_realtime_chat
logging_operation.clean_log_file() # For Debug
from data_entity import entity_manager
import data_entity

# # Test for operation_db.delete
# data_dict = {'message_id': 2, 'sender': None, 'receiver': None, 'content': None, 'time_generate': None, 'source': None}
# message = data_entity.entity_normalization.data_dict_to_entity(data_dict,data_entity.message.Message)
# operation_db.delete(message)

# # Test for operation_db.update
# data_dict = {'message_id': 2, 'sender': 0, 'receiver': 0, 'content': 'aaa', 'time_generate': '', 'source': 3}

# message = data_entity.entity_normalization.data_dict_to_entity(data_dict,data_entity.message.Message)
# print(message.time_generate)
# operation_db.update(message)




# print(operation_db.update(message))



# Test for operation_db.select
# print(operation_db.select(data_entity.message.Message,['message_id','sender']))

# # ----------------------------
# # Test for main_realtime_chat.chat_data_initial()
# operation_db.initial()
# main_realtime_chat.chat_data_initial()

# ----------------------------
# Test for recursionlimit
# sys.setrecursionlimit(100000)
# logging_operation.write_log(sys.getrecursionlimit(), source = __name__, level = 50)


# ----------------------------
# Test for entity_manager.get_entity_list_for_db_table()
# logging_operation.write_log(entity_manager.get_entity_list_for_db_table(), source = __name__, level = 50)



#-----------------------------
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# from data import data_classes
# Test for data_classes.New_Message.get_attribute_annotition()
# print(data_classes.New_Message.get_attribute_annotition())


#-----------------------------
# Test for python class alter to table column
# import sqlite3,datetime

# class Message():
#     # Attributes
#     message_id:str # 
#     sender:str # sender id
#     receiver:str # receiver id
#     content:dict # text / image file url / audio file url 
#     time_generate: datetime.datetime # the new born time of the message
#     source:str # chatbox / wechat / mail / windows mic / wearable mic
    
#     def __init__(self, id, sender, receiver, content, time_generate, source):
#         self.message_id = id
#         self.sender = sender
#         self.receiver = receiver
#         self.content = content
#         self.time_generate = time_generate
#         self.source = source
    
#     def __repr__(self) -> str:
#         pass
        
# message_list = [
#     Message()
    
# ]

# class Point:
    
    
#     def __init__(self, x, y):
#         self.x, self.y = x, y

#     def __repr__(self):
#         return f"Point({self.x}, {self.y})"

# def adapt_point(point):
#     return f"{point.x};{point.y}"

# def convert_point(s):
#     x, y = list(map(float, s.split(b";")))
#     return Point(x, y)

# # Register the adapter and converter
# sqlite3.register_adapter(Point, adapt_point)
# sqlite3.register_converter("point", convert_point)

# # 1) Parse using declared types
# p = Point(4.0, -3.2)
# con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
# cur = con.execute("CREATE TABLE test(p point)")

# cur.execute("INSERT INTO test(p) VALUES(?)", (p,))
# cur.execute("SELECT p FROM test")
# print("with declared types:", cur.fetchone()[0])
# cur.close()
# con.close()

# # 2) Parse using column names
# con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_COLNAMES)
# cur = con.execute("CREATE TABLE test(p)")

# cur.execute("INSERT INTO test(p) VALUES(?)", (p,))
# cur.execute('SELECT p AS "p [point]" FROM test')
# print("with column names:", cur.fetchone()[0])
















# from database import taskDBO

# '''
# db.initial()
# for task in db.selectAll(db.createConnection('asset/tasks/Task.db')):
#     print(task)
# '''

# conn = taskDBO.createConnection('asset/tasks/Task.db')

# items = taskDBO.selectAll(conn)
# print(items)