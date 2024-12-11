from multiprocessing import current_process

from capacities.basic.db import operation_db 
from capacities.basic.file import operation_file
from logs import logging_operation
import data_entity,data_entity.message

# shared data and threads
cross_process_data_zone = dict()
thread_list = list()

def chat_main(data_zone, sub_service_list):
    '''
        # Introduction
        Route the master instructions to the right capacities
        Called by service_main and managed by multiprocess_manager
    '''
    process = current_process()
    # shared data from crossing processes
    global cross_process_data_zone
    cross_process_data_zone = data_zone
    # services to run in this process
    global thread_list
    thread_list = sub_service_list
    
    # run the threads

def chat_data_initial():
    file_url_for_Message = "data\\message_for_test.csv"
    # Initial the message data
    ## Read message data to list of data_entity.message.Message 
    data_entity_list = operation_file.csv_to_data_entity(file_url_for_Message,data_entity.message.Message)
    logging_operation.write_log(f"data_entity_list rows are {data_entity_list.__len__()},{type(data_entity_list[1].message_id)}", source = __name__, level = 1)
    logging_operation.write_log(f"The current tables are \n{[data_entity.to_dict() for data_entity in data_entity_list ]}", source = __name__, level = 1)
    # insert into database
    if (not len(data_entity_list) == 0) and (not None in data_entity_list):
        operation_db.insert(data_entity_list)
  
    
def send_message():
    
    pass


def receive_message():
    pass