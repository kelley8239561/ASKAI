import inspect
import data_entity
from logs import logging_operation

def get_entity_list_for_db_table():
    '''
        # Introduction
        Search from the data_entity module to find all the classes need to convert to database table .
        
        # Returns
        (str, list[type]): (class_name, list of classes to be convert to database table)
    '''
    
    entity_list_for_db_table = None

    entity_list_all = inspect.getmembers(data_entity,inspect.isclass)
    entity_list_for_db_table = [entity for entity in entity_list_all if ((entity[1] in data_entity.basic_class.DB_Table.__subclasses__()) and (not len(entity[1].get_attribute_annotition()) == 0))]
    logging_operation.write_log(f"The entity list for db table is:\n{entity_list_for_db_table}", source = __name__, level = 1)
    
    return entity_list_for_db_table

def batch_initial_for_entity(class_type:type, column_list:list[str], data:list[tuple]):
    
    
    
    
    
    return
    
    
    
    