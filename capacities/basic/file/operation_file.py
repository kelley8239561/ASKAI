import traceback
from types import NoneType
import pandas,sys
from logs import logging_operation
from data_entity import entity_normalization, message
import data_entity.message
import numpy
from datetime import datetime
from capacities.basic.file import tp_file


def csv_to_data_entity(file_url:str,class_type:type) -> list:
    '''
        # Introduction
        Read csv files and parse the data to specified class
        
        # Params
        - file_url: the file url to read
        - class_type: the pecified class to parse
        
        # Returns
        list(class_type): the list of data class
    '''
    data_entity_list:list = list()
    # logging_operation.write_log(sys.getrecursionlimit(), source = __name__, level = 50)
    try:
        data_frame = pandas.read_csv(file_url,encoding='gbk')
        for row in data_frame.index:
            data_line = data_frame.iloc[row]
            data_line = data_line.replace({numpy.nan:None})
            # logging_operation.write_log("The data_line is \n" + str(data_line) + "\ntype:"+ str(type(data_line)), source = __name__, level = 1)
            try:
                logging_operation.write_log(f"The data_line is \n{data_line.to_dict()}", source = __name__, level = 1)
                logging_operation.write_log(f"The type of data_line is \n{[type(item[1]) for item in data_line.to_dict().items()]}", source = __name__, level = 1)
                data_entity = entity_normalization.data_dict_to_entity(data_line.to_dict(), class_type)
                if not (data_entity is None):
                    data_entity_list.append(data_entity)
                else:
                    logging_operation.write_log(f"Data line\n{data_line}\n can not parse to class {class_type}", source = __name__, level = 1)
            except Exception as e:
                logging_operation.write_log(f"Error occur when a line of data parse to class {class_type}\n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
    except Exception as e:
        logging_operation.write_log(f"Error occur when parse csv file {file_url} data to class \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
    return data_entity_list
  
def excel_to_data_entity(file_url,sheet_name,class_type):
    '''
        # Introduction
        Read csv files and parse the data to specified class
        
        # Params
        - file_url: the file url to read
        - class_type: the pecified class to parse
        
        # Returns
        list(class_type): the list of data class
    '''
    pass




