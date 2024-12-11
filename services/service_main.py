import os,time
from logs import logging_operation
from services import multiprocess_manager
from multiprocessing import (
    Process,
    Manager,
)
from capacities.basic import operation_km

def initial():
    '''
        # Introduction
        Quick initialization of ASKAI
    ''' 

def main():
    logging_operation.write_log("main service start...", source = __name__, level = 1)
    
    # multiprocess items initialize
    multiprocess_manager.initial()
    
    # hotkeys initial
    operation_km.initial_hotkeys()
    
    # processes initial
    process_list:list[Process] = multiprocess_manager.process_initial()
    logging_operation.write_log(f"Get the process_list {process_list.__len__()} \n{process_list}", source = __name__, level = 1)

    
    # start processes
    for process in process_list:
        # Call the start function
        process_start(process)
    
    # recycle processes
    for process in process_list:
        process.join(timeout=3)
        if process.is_alive():
            # if alive, add to the end of the queue
            process_list.append(process)
            # logging_operation.write_log(f"The process {process.name} is alive, the current process num is {process_list.__len__()}", source = __name__, level = 1)
        else:
            # not alive, recycle the current process and check the quit flag to determine if restart a new process
            # recycle the process
            process_quit(process)
            # verify quit flag to determine guard or not
            if not multiprocess_manager.cross_process_data_zone["service_control"]["service_main_quit"] and not multiprocess_manager.cross_process_data_zone["service_control"][process.name + "_quit"]:
                # reinitial and restart the process and add to the end of the queue
                for new_process in multiprocess_manager.process_initial(process.name):
                    process_start(new_process)
                    process_list.append(new_process)
            
    
    # logging_operation.write_log("main service ready to quit...", source = __name__, level = 1)

def service_main_quit():
    '''
        # Introduction
        Set the service_main_quit == True, this means the service_main is starting the quit procedure.
    '''
    # update the quit flag in the cross process data zone
    service_control = multiprocess_manager.cross_process_data_zone['service_control']
    service_control['service_main_quit'] = True
    multiprocess_manager.cross_process_data_zone['service_control'] = service_control
    logging_operation.write_log(f"Set the service_main_quit == {multiprocess_manager.cross_process_data_zone['service_control']['service_main_quit']}", source = __name__, level = 1)
    
def process_start(process:Process):
    '''
        # Information
        Start a process which is ready to start and update the infor in the multiprocess manager and the cross process shared zone
    
        # Params
        - process: the initialized process to start
    '''
    process.start()
    # update the basic infomation pid and state of the process in the multiprocess manager
    # update service state to activate and save the pid
    multiprocess_manager.update_running_services_param(process.name, 'pid', process.pid)
    multiprocess_manager.update_running_services_param(process.name, 'state', 'activate')
    # update the quit flag in the cross process data zone
    service_control = multiprocess_manager.cross_process_data_zone['service_control']
    service_control[process.name+'_quit'] = False
    multiprocess_manager.cross_process_data_zone['service_control'] = service_control
    logging_operation.write_log(
        f'''Start process {process.name}
        group:{multiprocess_manager.get_running_services_param(process.name,'group')}
        target:{multiprocess_manager.get_running_services_param(process.name,'target')}
        pid:{multiprocess_manager.get_running_services_param(process.name,'pid')}
        state:{multiprocess_manager.get_running_services_param(process.name,'state')}''', 
        source = __name__,
        level = 1
    )
    
def process_quit(process:Process):
    '''
        # Information
        Close a process which runs to the end. Update the information in the multiprocess manager and the cross process shared zone
    
        # Params
        - process: the process to quit
    '''
    process.close()
    # Update the information in the multiprocess manager. Set service state to stop
    multiprocess_manager.update_running_services_param(process.name, 'state', 'stop')
    logging_operation.write_log(
        f'''Quit process {process.name}
        group:{multiprocess_manager.get_running_services_param(process.name,'group')}
        target:{multiprocess_manager.get_running_services_param(process.name,'target')}
        pid:{multiprocess_manager.get_running_services_param(process.name,'pid')}
        state:{multiprocess_manager.get_running_services_param(process.name,'state')}''', 
        source = __name__,
        level = 1
    )
