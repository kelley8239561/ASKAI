import time
from logs import logging_operation
from multiprocessing import current_process
from realtime_chat import listener

# shared data and threads
cross_process_data_zone = dict()
thread_list = list()


def router_main(data_zone,sub_service_list):
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
    
    # Get instructions and save in the instruction_list
    instruction_list = list(dict)
    ## *1. From chatbox 
    chat_data_chatbox = listener.get_chatbox_message()
    
    ## 2. From computer mic
    
    ## *3. From wearable mic

    ## *4. From wechat
    
    ## 5. From mail
    
    # Task Extraction
    
    
    # Task Planning
    
    
    # Task Executation
    
    
    
    
    
    
    while not cross_process_data_zone["service_control"]["service_main_quit"]:
        time.sleep(1)
        logging_operation.write_log(f"In {__name__}, the quit flag is {cross_process_data_zone["service_control"]["service_main_quit"]}", source = __name__, level = 1)
    
    
    
    
    
        
    # update the quit flag in the cross process data zone
    service_control = cross_process_data_zone['service_control']
    service_control[process.name+'_quit'] = True
    cross_process_data_zone['service_control'] = service_control
    logging_operation.write_log(f"{process.name} service works all done, back to service_main and set the {process.name}_quit flag True", source = __name__, level = 1)    
    