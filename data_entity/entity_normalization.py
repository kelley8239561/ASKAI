import traceback
from types import NoneType
from logs import logging_operation
import data_entity
from data_entity import message,user,task

def data_dict_to_entity(origin_data:dict,class_type:type):
    '''
        # Introduction
        Normalize the type of each dict value in origin_data and form a entity of class_type.
        
        # Params
        - origin_data: the original data waiting to normalize
        - class_type: the target class to initial
        
        # Returns
        - None: if normalize failed
        - data_list: the result of the successful normalization
    '''
    # Call function class_type.tn_all(func tn_all of class 'class_type')
    data_entity = None
    try:
        logging_operation.write_log(f"Parse dict \n{origin_data}\nto {class_type}", source = __name__, level = 1)

        if (normal_data := class_type.tn_all(origin_data))[0]:
            data_entity = class_type(normal_data[1])
        else:
            logging_operation.write_log(f"Error occur when parse data to {class_type}, the unparseble data is:\n{origin_data}", source = __name__, level = 1)
            
    except Exception as e:
        logging_operation.write_log(f"Error occur when a line of data parse to class {class_type}\n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
    
    return data_entity

def data_dict_list_to_entity_list(origin_data_list:list[dict],class_type:type):
    '''
        # Introduction
        Parse each line of origin_data_list to form a entity list of class_type.
        
        # Params
        - origin_data_list: the original data list waiting to normalize
        - class_type: the target class to initial
        
        # Returns
        - data_entity_list: the result of the successful normalization of the origin_data_list
    '''
    data_entity_list = list()
    
    for origin_data in origin_data_list:
        # Call data_dict_to_entity
        data_entity = data_dict_to_entity(origin_data,class_type)
        if not data_entity is None:
            data_entity_list.append(data_entity)
    
    return data_entity

def data_list_to_entity_list(column_list:list[str], origin_data_list:list[tuple], class_type:type,):
    data_entity_list = list()
    if origin_data_list:
        for origin_data in origin_data_list:
            data_dict = dict(zip(column_list,origin_data))
            data_entity = data_dict_to_entity(data_dict,class_type)
            if not data_entity is None:
                data_entity_list.append(data_entity)
    
    return data_entity_list