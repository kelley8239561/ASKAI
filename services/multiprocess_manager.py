from multiprocessing import (
    Process,
    Manager,
)
from threading import Thread
from config import config_operations
from logs import logging_operation
import services, debug
import debug.service_test
import services.service_router


# share zone for multiprocess communication and data share
cross_process_data_zone = None

# The flag space to maintain the service info
service_list = list()

def initial():
    '''
        # Introduction
        Initial the following items: 
        1. Data zone: which is shared between processes
        2. Service infomation: Get from the configuration file. Which is used for process and thread initial.
    '''
    # Services configuration initial
    global service_list
    service_list = get_running_services_config()['config_content']
    # Sort by group(smaller in the front) and main(False in the front)
    n = len(service_list)
    for i in range(n):
        for j in range(n-i-1):
            if int(service_list[j]['group']) > int(service_list[j+1]['group']):
                service_list[j], service_list[j+1] = service_list[j+1], service_list[j]
            elif int(service_list[j]['group']) == int(service_list[j+1]['group']):
                if not service_list[j+1]['main']:
                    service_list[j], service_list[j+1] = service_list[j+1], service_list[j]
    logging_operation.write_log(f"Initial service_list.\n{service_list}", source = __name__, level = 1)
    
    # Data zone initial
    global cross_process_data_zone
    cross_process_data_manager = Manager()
    cross_process_data_zone = cross_process_data_manager.dict(
        {
            "service_control": {
                "service_main_quit": False, # global quit flag
            },  
            "service_info": [], # processes and threads info and state
        }
    )
    logging_operation.write_log(f"Initial the data zone.\n{cross_process_data_zone}", source = __name__, level = 1)

def process_initial(process_name:str = None):
    '''
        # Introduction
        According to the running service configuration, have the processes ready for running.
        
        # Param
        - proess_name: name of the target process to initialize. None means all.
        
        # Returns
        - list(Process): list of Processes which are ready to run.
        - None: No process is ready to run.
    '''
    global service_list
    process_list:list[Process] = list()
    sub_service_list:list[dict] = list()
    
    if service_list.__len__() == 0:
        logging_operation.write_log("No services is ready to run. Please check the running_services.yaml.", source = __name__, level = 1)
        return # No process
    
    # Create the processes and pass the sub_process(thread)
    for service in service_list:  
        if service['main']:
            if not process_name:
                # process_name = None, get all processes ready
                # logging_operation.write_log(f"Create process {service['name']} {service['target']} {type(service['target'])}", source = __name__, level = 1)
                process = Process(name = service['name'], target = eval(service['target']), args=(cross_process_data_zone,sub_service_list,))    
                update_running_services_param(service['name'], 'state', 'ready')
                sub_service_list = list()
                process_list.append(process)
            elif process_name and service['name'] == process_name:
                # process_name is not None, get the 'process_name' process ready
                # logging_operation.write_log(f"Create process {service['name']} {service['target']} {type(service['target'])}", source = __name__, level = 1)
                process = Process(name = service['name'], target = eval(service['target']), args=(cross_process_data_zone,sub_service_list,))    
                update_running_services_param(service['name'], 'state', 'ready')
                sub_service_list = list()
                process_list.append(process)
        else:
            sub_service_list.append(service)
    return process_list

def thread_initial(process_name:str, thread_name:str = None):
    '''
        # Introduction
        According to the running service configuration and the process_name, have the related thread ready for running.
        
        # Param
        - proess_name: name of the process which the target thread belong to.
        - thread_name: name of the target thread. None means get all
    '''
    thread_list:list[Thread] = list()
    global service_list
    
    # Get target Process group
    for service in service_list:
        if service['name'] == process_name:
            service_group = service['group']
            break
    
    # Get target Thread list
    for service in service_list:
        if service['group'] == service_group:
            if not thread_name:
                thread = Thread(name=service['name'], target = eval(service['target']))
                thread_list.append(thread)
                # logging_operation.write_log(f"Create Thread {service['name']} {service['target']} {type(service['target'])}", source = __name__, level = 1)
                update_running_services_param(service['name'], 'state','ready')
            elif thread_name and service['name'] == thread_name:
                thread = Thread(name=service['name'], target = eval(service['target']))
                thread_list.append(thread)
                # logging_operation.write_log(f"Create Thread {service['name']} {service['target']} {type(service['target'])}", source = __name__, level = 1)
                update_running_services_param(service['name'], 'state', 'ready')
    return thread_list

def get_running_services_config():
    '''
        # Introduction
        Get process config from the config file
        The process config name is 'running_services'
    '''
    running_services_config:dict = None
    # logging_operation.write_log("Get running_services configuration", source = __name__, level = 1)
    for config_data in config_operations.get_config(__name__):
        # config_name == running_services
        if config_data['config_name'] == 'running_services':
            running_services_config = config_data
            break
    
    return running_services_config

def get_running_services_param(service_name:str, param_name:str):
    '''
        # Introduction
        Get the target parameter value of the service
        
        # Params
        - service_name: the target service to get
        - param_name: the target parameter to get
        
        # Returns
        - param_value: the value of the target parameter 'param_name'
        - None:
            - No parameter named 'param_name'
            - No service named 'service_name' 
    '''
    global service_list
    for service in service_list:
        if service['name'] == service_name:
            param_value = service[param_name]
            
    return param_value

def update_running_services_param(service_name:str, param_name:str, param_value:any):
    '''
        # Introduction
        Set the state of a service to 'state' in the running_services.yaml file
        
        # Param
        - service_name: The service to set state to
        - param_name: The effective param name are:
            - state, pid, tid
        - value: target value of the 'param_name' param
            - state:ready,activate,suspend,stop
            - pid:integer
            - tid:integer
        
        # Returns
        - True: Success
        - None: 
            - Can not find the service 'service_name'
            - Illegal param_name
            - Illegal value
    '''
    global service_list
    # safety check the param_name
    if param_name in ['state','pid','tid']:
        for service in service_list:
            if service['name'] == service_name:
                service[param_name] = param_value
                return True
    return
    
def add_running_service(new_service:dict):
    '''
        # Introduction
        Add service info to the service list
        # Param
    '''
    global service_list
    for service in service_list:
        if service['name'] == new_service['name']:
            # update
            pass
    pass



