from logs import logging_operation
import time,os
from multiprocessing import current_process
# shared data
cross_process_data_zone = None

def test_main(data_zone,sub_service_list):
    # get the current process class entity
    process = current_process()
    logging_operation.write_log(f"{process.name} service is going to work.......", source = __name__, level = 1)
    global cross_process_data_zone
    cross_process_data_zone = data_zone
    
    # logging_operation.write_log("Wait for 5 second.", source = __name__, level = 1)
    time.sleep(5)
    if not process.name == 'chat_service':
        # update the quit flag in the cross process data zone
        service_control = cross_process_data_zone['service_control']
        service_control[process.name+'_quit'] = True
        cross_process_data_zone['service_control'] = service_control
    
    logging_operation.write_log(f"{process.name} service works all done, back to service_main and set the {process.name}_quit flag True", source = __name__, level = 1)