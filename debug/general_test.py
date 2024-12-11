# ---------------------------------
# sys.path, import
import sys
print(sys.path)



# # # ---------------------------------
# # # None to str
# a = None
# b = str(a)
# print(b,type(b))
# if b == 'None':
#     print(1111)

# a = ''
# b = str(a)
# print(b,type(b))
# if b == '':
#     print(2222)



# # # ---------------------------------
# # Test for Message.primary_key()
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# import data_entity

# a =data_entity.message.Message(None)
# print(data_entity.message.Base.primary_key())
# print(a.to_dict())



# # ---------------------------------
# # list
# key = ['a','b','c']
# value = (1,"222",3.1)

# print(dict(zip(key,value)))



# # ---------------------------------
# # list
# a = list()
# a = None
# if a:
#     for a_child in a:
#         print(111)

# b = "12345"
# c = ""
# c = f"{c} {b}"
# c = c[1:]
# print(b)


# # ---------------------------------
# # Test for Message.message_id
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# import data_entity
# data_dict = {'message_id': None, 'sender': 2, 'receiver': 1, 'content': 'houhou', 'time_generate': '2024/9/13 14:50:00', 'source': 4}
# message = data_entity.message.Message(data_dict)
# print(message.message_id)

# # ---------------------------------
# # multi class
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# import data_entity
# # import data_entity.message
# print(data_entity.message.Message.__base__,data_entity.message.Message.__bases__)
# print(len(data_entity.user.User.get_attribute_annotition()))

# # ---------------------------------
# # multi class
# class A:
#     def a(self):
#         print(111)
# class B:
#     def a(self):
#         print(222)       
# class C(A, B):
#     pass
# c = C()
# c.a()

# class A:
#     def a(self):
#         print(111)
# class B(A):
#     def a(self):
#         print(222) 
# class C(B):
#     pass
# c = C()
# c.a()


# # ---------------------------------
# # convert None
# a = None
# b = int(a)
# print(b)



# # ---------------------------------
# # __subclasses()__
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# import data_entity
# # import data_entity.message
# # import data_entity.task
# # print(data_entity.basic_class.DB_Table.__subclasscheck__(data_entity.message.Message))
# print(data_entity.basic_class.DB_Table.__subclasses__())
# print(data_entity.basic_class.DB_Table.get_child_class())

# # ---------------------------------
# # :=
# def plus(a,b):
#     return a+b
# if (result := plus(3,2)) == 5:
#     haha = result
# print(haha)

# # ---------------------------------
# # if None
# # list() == None
# if not None:
#     print(111)
    
# if 111:
#     print(222)
    
# if not '':
#     print(333)
    
    
# a = list()
# print(a)
# if a == None:
#     print(444)

# # ---------------------------------
# # test for get_type_normalization_function
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# import data.data_class

# # print(data.data_class.Message.get_type_normalization_function('message_id'))
# # print(data.data_class.New_Message.get_type_normalization_function('message_id'))
# # print(data.data_class.Message.get_type_normalization_function('owner'))
# # print(data.data_class.New_Message.get_type_normalization_function('owner'))

# # a = data.data_class.Message.get_type_normalization_function('message_id')('2')
# # print(a)
# data_dict = {'message_id': 9, 'sender': 2, 'receiver': 1, 'content': 'houhou', 'time_generate': '2024/9/13 14:50:00', 'source': 4}
# message = data.data_class.Message(data_dict)
# print(message.get_type_normalization_function('message_id'))



# # ---------------------------------
# # test for get_class_methods
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# import data.data_class

# print(data.data_class.New_Message.get_class_method())
# print(data.data_class.New_Message.accept_None())
# print(data.data_class.Message.accept_None())

# print(data.data_class.New_Message.primary_key())
# print(data.data_class.Message.primary_key())

# print(data.data_class.New_Message.auto_increase())
# print(data.data_class.Message.auto_increase())


# # ---------------------------------
# # @classmethod
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# import data.data_class

# a = data.data_class.Base(None)
# print(a.to_dict())



# # ---------------------------------
# # dict no keys
# a = {'a':1}
# print(a['a'])
# print(a['b'])


# # ---------------------------------
# # list extend
# # https://blog.csdn.net/henanlion/article/details/138582542
# a = [1,2,3]
# b = [4,5,6]
# c = []
# a.extend(b)
# print(a,b)
# c.extend(a+b)
# print(c)



# # ---------------------------------
# # class attribute dict
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# from capacities.basic.file import entity
# from data import data_class
# class_entity = data_class.Message
# attribute_str = 'message_id'
# a = entity.file_to_class_entity[class_entity][attribute_str]
# print(a(10))

# ---------------------------------
# DataFrame.fillna
# import pandas
# data = pandas.DataFrame()
# data.fillna(value=None, method=None, axis=None, inplace=False, limit=None, downcast=None, **kwargs)


# # ---------------------------------
# # None, NoneType isinstance
# from types import NoneType
# a = None
# print(isinstance(a,NoneType))
# print(isinstance(a,(NoneType,int,float)))
# print(isinstance(a,(int,float)))
# print(a is None)
# print(a is NoneType)
# print(type(a) is NoneType)


# # ---------------------------------
# # numpy type
# import numpy
# a = numpy.int64(1111111111111111111)
# b = int(1111111111111111111)
# c = numpy.int32(111111111)
# print(type(a),type(b),type(c))
# print(isinstance(c,numpy.int32))
# a = numpy.float64(1.1)
# b = numpy.float_(2.1)
# print(isinstance(a,numpy.float_))
# print(a,type(a))
# print(b,type(b))
# c = int(2)
# d = numpy.int16(2)
# e = numpy.int32(2)
# f = numpy.int64(2)
# g = numpy.int_(2)
# print(isinstance(c,numpy.int_),type(c))
# print(isinstance(d,numpy.int_),type(d))
# print(isinstance(e,numpy.int_),type(e))
# print(isinstance(f,numpy.int_),type(f))
# print(isinstance(g,numpy.int_),type(g))




# d = int(a)
# c = numpy.int32(a)
# print(d,type(d))
# print(c,type(c))


# # ---------------------------------
# # class initial
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# from data import data_class
# from logs import logging_operation
# logging_operation.clean_log_file() # For Debug
# class_type = data_class.Message
# data_dict = {'message_id': 9, 'sender': 2, 'receiver': 1, 'content': 'houhou', 'time_generate': '2024/9/13 14:50:00', 'source': 4}
# message = data_class.Message(data_dict)
# print(message.to_dict())
# print(message.time_generate,type(message.time_generate))

# # ---------------------------------
# # str and datetime
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# from datetime import datetime
# from capacities.basic.file import entity
# str = '2024/9/13 14:50:20'
# result = entity.tp_str_to_datetime(str)
# print(result,type(result))


# # ---------------------------------
# # exec
# a = 3
# b = 0
# exec("b=a")
# print(b)
# eval
# a = 3
# b = 0
# b = eval("a+b")
# print(b)


# # ---------------------------------
# # pandas.DataFrame
# # https://blog.csdn.net/codeljy/article/details/90453855
# # https://www.cnblogs.com/tonorth123/p/11462691.html
# import pandas
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# url = 'data\\message\\message_for_test.csv'
# url1 = 'data\\message\\message_for_test.xlsx'
# df = pandas.read_csv(url,encoding='gbk')
# # print(df,type(df)) # dataframe
# # print(df.index,type(df.index)) # index

# # for i in df.index:
# #     # index usage to literal
# #     print(i,type(i))

# # DataFrame.iloc
# data_line = df.iloc[0] 
# print(data_line,type(data_line))
# # print(data_line.iloc[0],type(data_line.iloc[0])) # Series.iloc
# # print(data_line.index,type(data_line.index)) # Series.index
# # print(data_line.to_dict(),type(data_line.to_dict())) # Series.to_dict
# print(data_line['time_generate'],type(data_line['time_generate']))





# # ---------------------------------
# # pandas read_excel read_csv
# import pandas,codecs,chardet
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# url = 'data\\message\\message_for_test.csv'
# url1 = 'data\\message\\message_for_test.xlsx'
# # with open(url, 'rb') as f:
# #     data = f.readline()
# #     result = chardet.detect(data)
# #     print(result)
# # with open(url,'r', encoding='gbk',errors='replace') as f:
# #     data = f.read()
# #     print(data)
# df = pandas.read_csv(url,encoding='gbk')
# for df_line in df:
#     print(df_line,type(df_line))
# df1 = pandas.read_excel(url1,sheet_name=[0,1])
# print(df1[0].head(10))

# # ---------------------------------
# # str index end
# a = 'abcd'
# b = a[:-1]
# print(b)

# # ---------------------------------
# # class attribute
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# from data import data_classes

# print(vars(data_classes.Base))


# # ---------------------------------
# # f string nest structure
# a = "CREATE TABLE {table_name} ({column_list})"
# table_name = '111'
# column_list = '222'
# b = a.format(table_name = table_name,column_list = column_list)
# print(b)




# # ---------------------------------
# # f string nest structure
# a = '111'
# b = '222'
# print(f"hahahaha{str(f'{a} {b}')}")

# # ---------------------------------
# # dict items()
# dict_test = {
#     'a':1,
#     'b':2,
# }

# for item in dict_test.items():
#     print(item,type(item))


# # ---------------------------------
# # inspect.getmembers, inspect.isclass, substr in str
# import inspect
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# import data_entity


# entity_list = inspect.getmembers(data_entity,inspect.isclass)
# print([entity[0] for entity in entity_list if entity[1] in data_entity.basic_class.DB_Table.__subclasses__()])



# print(list)
# print([(a[1],type(a[1])) for a in inspect.getmembers(data_entity,inspect.isclass) if 'data.data_classes.'in str(a[1])])
# entity_module_url = data.data_classes
# print(entity_module_url,type(entity_module_url))
# print(entity_module_url.__name__)

# # ---------------------------------
# # Enum
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# from data import basic_class
# a = basic_class.Message_Source(1)
# print(a,type(a),a.value,a.name)
# b = basic_class.Message_Source(4)
# print(b,type(b))


# # ---------------------------------
# # Enum
# from enum import Enum
# class Member(Enum):
#     wechat = 1
#     chatbox = 2
#     mail = 3

# member = Member(1)
# print(member,type(member))
# print(member.value)
# print(member.name)


# # ---------------------------------
# # enumerate
# a = enumerate(['a','b','c'])
# for a_child in a:
#     print(a_child)



# # ---------------------------------
# # dict key type
# # traceback
# # Exception
# import traceback
# db_type_map = {
#     str:'TEXT',
# }
# try:
#     print(db_type_map[str])
#     print(db_type_map['str'])
# except Exception as e:
#     print(e.__class__,e)
#     traceback.print_exc()

# # ---------------------------------
# # list filter
# b = [str(a) for a in [1,2,3,4,5] if a < 5]
# name = "haha {ha}"
# print(b)
# print(str(b))
# print(name.format(ha = b))

# # ---------------------------------
# # dict update
# a = {'haha':1,'gaga':2}
# b = {'hehe':3,'haha':5}
# a.update(b)
# b.update(a)
# print(a)
# print(b)

# # ---------------------------------
# # the type of a class defination
# # dirs(): list of attributes of an object
# # vars(): list of attributes and values of an object
# # locals() and globals(): list of attributes and values of local / global
# class People:
#     def __init__(self, name, age) -> None:
#         self.name = name
#         self.age = age
#     name:str
#     age:int
# class Student(People):
#     def __init__(self, name, age, sid) -> None:
#         super().__init__(name, age)
#         self.sid = sid
#     sid:int
# student = Student('a',16,1314)
# print(dir(Student))
# print(vars(Student))
# print(locals())
# print(dir(Student))
# print(vars(student))
# print(People.__base__.__base__)
# print(Student.__base__.__base____annotations__)



# # ---------------------------------
# # the type of a class defination
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# from data.message import data_structure
# print(type(str))
# print(type(data_structure.New_Message))


# # ---------------------------------
# # keyboard,hotkey,get hotkeys
# import keyboard
# def a():
#     print('a')
    
# def b():
#     print('b')

# keyboard.add_hotkey('a',callback=a)
# keyboard.add_hotkey('b',callback=b)
# print(keyboard._hotkeys.keys())

# ---------------------------------
# # multiprocessing
# # Get the process name by using multiprocessing.current_process().name
# from multiprocessing import Process,current_process
# def do():
#     print(current_process().name)
    
# if __name__ == "__main__":
#     process = Process(name='new worker',target = do,args=())
#     process.start()
#     process.join()
#     print(current_process().name)
#     print("end")

# ---------------------------------
# file delete by lines
# import sys
# sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
# # print(sys.path)
# from logs import logging_operation
# if __name__ == '__main__':
#     logging_operation.clean_log_file(0,50)

# ---------------------------------
# # return
# # The default value of return is None
# def return_test():
#     return
# print(return_test())

# ---------------------------------
# # yaml load() and safeload()
# import yaml
# with open('config/running_services.yaml', 'r') as f:
#     data1 = yaml.safe_load(f)
#     data2 = yaml.load(f,Loader=yaml.FullLoader)

# data1['config_content'] = 0
# with open('config/running_services.yaml', 'w') as f:
#     yaml.safe_dump(data1,f)

# ---------------------------------
# # list动态添加
# import time
# name_list = [1,2,3,4]
# temp_name = 5
# for name in name_list:
#     if temp_name <= 10:
#         name_list.append(temp_name)
#         temp_name = temp_name + 1
#     time.sleep(1)
#     print(name)

# ---------------------------------
# # dict
# # 验证重复的key是否可以获取多个value：不可以，获取的是最后一个
# config_file_urls = {
#     'services.multiprocess_manager': 'config/running_services.yaml',
#     'services.multiprocess_manager': 'config/voiceListenServiceConfig.yaml',
#     'services.multiprocess_manager': 'config/screenRecordServiceConfig.yaml'
# }
# while None:
#     print(config_file_urls['services.multiprocess_manager'])