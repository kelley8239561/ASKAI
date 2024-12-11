from datetime import datetime
import traceback
import numpy
import data_entity.basic_structure,data_entity.message
import types
from logs import logging_operation

'''
Functions for type parsing serve for file operation
- tp for type parsing

'''

# ------------------------------
# Basic type parsing

datetime_format = [
    "%Y/%m/%d %H:%M:%S",
    "%d/%m/%Y %H:%M:%S",
    "%Y-%m-%d",
    "%d/%m/%Y",
]

def tp_str_to_datetime(origin_value:str):
    '''
        # Introuction
        Parse type str to datetime.datetime
        
        
        # Params
        - origin_value: type str, the value waiting to parse
            The accept formate including
            - "%Y/%m/%d %H:%M:%S",
            - "%d/%m/%Y %H:%M:%S",
            - "%Y-%m-%d",
            - "%d/%m/%Y",
        
        # Returns
        - None: fail to parse
        - target value: type datetime.datetime
    '''
    
    global datetime_format
    target_value = None
    for format in datetime_format:
        try:
            target_value =  datetime.strptime(origin_value, format)
            break
        except Exception as e:
            logging_operation.write_log(f"Do not match type {format}", source = __name__, level = 1)
            continue
    return target_value

def tp_int_to_Message_Source(origin_value:int):
    '''
        # Introuction
        Parse type int to data_entity.basic_structure.Message_Source
        
        # Params
        - origin_value: type int, the value waiting to parse
        
        # Returns
        - None: fail to parse
        - target value: data_entity.basic_structure.Message_Source
    '''
    target_value = None
    try:
        target_value = data_entity.basic_structure.Message_Source(origin_value)
    except Exception as e:
        logging_operation.write_log(f"Type parsing error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
    
    return target_value 

def tp_number_to_int(origin_value):
    '''
        # Introuction
        Parse type int to data_entity.basic_structure.Message_Source
        
        # Params
        - origin_value: type int, the value waiting to parse
        
        # Returns
        - None: fail to parse
        - target value: data_entity.basic_structure.
        
        Message_Source
    '''
    target_value = None
    try:
        target_value =  int(origin_value)
    except Exception as e:
        logging_operation.write_log(f"Type parsing error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)

    return target_value

number_type = [
    float, numpy.float32, numpy.float64, numpy.float16,
    int, numpy.int16, numpy.int32, numpy.int64, numpy.int8, numpy.int_, numpy.intc,
    bool, numpy.bool_,
]

def is_number_type(type_to_check:type):
    '''
        # Introuction
        Check if the type_to_check is a number type
        
        # Params
        - type_to_check: type, the type waiting to check
        
        # Returns
        - True: the type_to_check is a number type
        - False: the type_to_check is not a number type
    '''
    global number_type
    result = False
    if type_to_check in number_type:
        result = True
    return result
    
def tp_str_to_number(origin_value):
    '''
        # Introuction
        
        # Params
        - origin_value: type int, the value waiting to parse
        
        # Returns
        - None: fail to parse
        - target value: data_entity.basic_structure.Message_Source
    '''
    target_value = None
    try:
        target_value =  str(origin_value)
    except Exception as e:
        logging_operation.write_log(f"Type parsing error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)

    return target_value

def is_None_value(value_to_check):
    check_result = False
    if value_to_check == None:
        check_result = True
    elif isinstance(value_to_check,str) and value_to_check == '':
        check_result = True
    return check_result
    
    

