
from datetime import datetime
from typing import Any
from logs import logging_operation
from data_entity import basic_structure
from data_entity.basic_class import Base, DB_Table
from capacities.basic.file import tp_file
import traceback

class Message(Base, DB_Table):
    '''
        # Introduction
        The message sended or received from human-beings or robot 
        
        # Attributes
        
        # Functions
    
    '''
    # Attributes
    message_id:int # primary key
    sender:int # sender id
    receiver:int # receiver id
    content:str # text / image file url / audio file url 
    time_generate:datetime  # the new born time of the message
    source:basic_structure.Message_Source # chatbox / wechat / mail / windows mic / wearable mic
    
    def __init__(self, attribute_dict:dict):
        logging_operation.write_log(f"In class {__class__} __init__()", source = __name__, level = 1)

        initial_attribute_list = __class__.__annotations__.items()
        for initial_attribute in initial_attribute_list:
            if not attribute_dict.get(initial_attribute[0],"No keys") == "No Keys":
                logging_operation.write_log(f"{__class__}.{initial_attribute[0]} Initialing!", source = __name__, level = 1)

                exec(f"self.{initial_attribute[0]} = attribute_dict['{initial_attribute[0]}']")
                # eval(f"self.{initial_attribute[0]}") = attribute_dict[initial_attribute[0]]
                attribute_dict.pop(initial_attribute[0])
        if not(len(attribute_dict) == 0):
            super().__init__(attribute_dict)
        
        logging_operation.write_log(f"{__class__}Initial over!", source = __name__, level = 1)

    @classmethod
    def primary_key(cls):
        '''
            # Introduction
            Get the primary key attribute name of the class entity
            
            # Returns
            The string name of the primary key
        '''
        primary_key:str = 'message_id'
        return primary_key
    
    @classmethod
    def auto_increase(cls):
        '''
            # Introduction
            Get the auto_increase attribute name list of the class entity
            
            # Returns
            The list of the attribute name that are auto increase
        '''
        auto_increase_list:list = Message.__base__.auto_increase()
        auto_increase_list.extend(['message_id'])
        return auto_increase_list
    
    @classmethod
    def accept_None(cls):
        '''
            # Introduction
            Get the attribute name list of the class entity which can be None
            
            # Returns
            The list of the attribute name which can be None
        '''
        accept_None_list:list = Message.__base__.accept_None()
        accept_None_list.extend(['message_id','sender','receiver','content','time_generate','source'])
        # logging_operation.write_log(f"Message, acc{accept_None_list}", source = __name__, level = 1)
        return accept_None_list
        
    @classmethod
    def get_type_normalization_function(cls, attribute_name:str):
        '''
            # Introduction
            Search for type normalization function for the attribute by attribute_name
            
            # Params
            - attribute_name: the name of the attribute to search, type str
            
            # Returns
            - None: fail to search
            - Function call: of the target function
            
        
        '''
        function_call = None
        function_call_str = f"tn_{attribute_name}"
        if function_call_str in cls.get_class_function():
            function_call = eval(f"cls.{function_call_str}")
        return function_call
    
    @classmethod
    def tn_message_id(cls, origin_value):
        '''
            # Introduction
            Parse origin_value to Int
        '''
        target_value = None
        try:
            target_value = int(origin_value)
        except Exception as e:
            logging_operation.write_log(f"Type parsing error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
        return target_value

    @classmethod
    def tn_sender(cls, origin_value):
        '''
            # Introduction
            Parse origin_value to Int
        '''
        target_value = None
        try:
            target_value = int(origin_value)
        except Exception as e:
            logging_operation.write_log(f"Type parsing error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
        return target_value

    @classmethod
    def tn_receiver(cls, origin_value):
        '''
            # Introduction
            Parse origin_value to Int
        '''
        target_value = None
        try:
            target_value = int(origin_value)
        except Exception as e:
            logging_operation.write_log(f"Type parsing error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
        return target_value

    @classmethod
    def tn_content(cls, origin_value):
        '''
            # Introduction
            Parse origin_value to str
        '''
        target_value = None
        try:
            target_value = str(origin_value)
        except Exception as e:
            logging_operation.write_log(f"Type parsing error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
        return target_value

    @classmethod
    def tn_time_generate(cls, origin_value):
        '''
            # Introduction
            Parse origin_value to datetime.datetime
        '''
        target_value = None
        try:
            if isinstance(origin_value,str):
                # str to datetime.datetime
                if not (tp_result:=tp_file.tp_str_to_datetime(origin_value)) == None:
                    target_value = tp_result
                else:
                    logging_operation.write_log(f"Can not parse str value {origin_value} to datetime \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
                    return target_value
            else:
                logging_operation.write_log(f"Can not parse type {type(origin_value)} to datetime \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
                return target_value
        except Exception as e:
            logging_operation.write_log(f"Type parsing error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
        return target_value

    @classmethod
    def tn_source(cls, origin_value):
        '''
            # Introduction
            Parse origin_value to data.basic_data.Message_Source
        '''
        target_value = None
        try:
            if isinstance(origin_value,int):
                target_value = tp_file.tp_int_to_Message_Source(origin_value)
            elif tp_file.is_number_type(type(origin_value)):
                target_value = tp_file.tp_int_to_Message_Source(tp_file.tp_number_to_int(origin_value))
            else:
                logging_operation.write_log(f"Can not parse type {type(origin_value)} to str \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
                return target_value
        except Exception as e:
            logging_operation.write_log(f"Type parsing error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
        return target_value
             
class New_Message(Message, DB_Table):
    '''
        # Introduction
        The message sended or received from human-beings or robot 
        
        # Attributes
        
        # Functions
        
    '''
    owner:str # the user id of the message
    out_of_date:float # the message will be out of date afer this time span 
    
    def __init__(self, attribute_dict:dict):
        logging_operation.write_log(f"In class {__class__} __init__()", source = __name__, level = 1)

        initial_attribute_list = __class__.__annotations__.items()
        for initial_attribute in initial_attribute_list:
            if not attribute_dict.get(initial_attribute[0],"No keys") == "No Keys":
                exec(f"self.{initial_attribute[0]} = attribute_dict['{initial_attribute[0]}']")
                # eval(f"self.{initial_attribute[0]}") = attribute_dict[initial_attribute[0]]
                attribute_dict.pop(initial_attribute[0])
        if not(len(attribute_dict) == 0):
            super().__init__(attribute_dict)
        
        logging_operation.write_log(f"{__class__}Initial over!", source = __name__, level = 1)
        
    @classmethod
    def accept_None(cls):
        '''
            # Introduction
            Get the attribute name list of the class entity which can be None
            
            # Returns
            The list of the attribute name which can be None
        '''
        # logging_operation.write_log(f"New_Message, {cls.__base__.accept_None()}", source = __name__, level = 1)
        accept_None_list:list = New_Message.__base__.accept_None()
        accept_None_list.extend(['owner','out_of_date'])
        return accept_None_list    
    
    @classmethod
    def tn_owner(cls, origin_value):
        '''
            # Introduction
            Parse origin_value to str
        '''
        target_value = None
        try:
            target_value = str(origin_value)
        except Exception as e:
            logging_operation.write_log(f"Type parsing error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
        return target_value

    @classmethod
    def tn_out_of_date(cls, origin_value):
        '''
            # Introduction
            Parse origin_value to datetime.datetime
        '''
        target_value = None
        try:
            if isinstance(origin_value,str):
                # str to datetime.datetime
                target_value = tp_file.tp_datetime_to_str(origin_value)
            else:
                logging_operation.write_log(f"Can not parse type {type(origin_value)} to str \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
                return target_value
        except Exception as e:
            logging_operation.write_log(f"Type parsing error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
        return target_value        
            
            