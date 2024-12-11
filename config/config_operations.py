"""
    # _summary_
    Operations for getting configuration data
"""


import os, yaml
from logs import logging_operation

# urls and reading auth management
config_file_urls = {
    'services.multiprocess_manager': ['config/running_services.yaml',],
    'a': ['config/voiceListenServiceConfig.yaml',],
    'b': ['config/screenRecordServiceConfig.yaml',],
}

# for global use
config_data_list_global = dict()


def find_config_by_config_name(config_name):
    '''
        # Introduction
        find config data by config_name
        
        # Params
        - config_file_url: Whole relative path of the config file  
    '''
    global config_data_list_global
    for config_item in config_data_list_global.items():
        if config_item['config_name'] == config_name:
            return config_item
    return None

def find_config_by_file_url(config_file_url):
    '''
        # Introduction
        find config data by config_file_url
        
        # Params
        - config_file_url: Whole relative path of the config file  
    '''
    global config_data_list_global
    if config_file_url in config_data_list_global.keys():
        return config_data_list_global[config_file_url]
    else:
        return None

def get_config(caller:str = None):
    '''
        # Introduction
        Get config data by caller 
        
        # Params
        - caller: Use caller to get the authorized config urls. Typically caller is '__name__' of the calling file
    '''
    global config_data_list_global
    config_data_list: list[dict] = list()
    
    if caller:
        file_urls = config_file_urls[caller]
        for url in file_urls:
            config_data = find_config_by_file_url(url)
            if config_data:
                # Return directly if in config_data_list_global
                config_data_list.append(config_data)
            else:
                # Read file and return the reading result
                with open(url,'r') as file:
                    config_data = yaml.safe_load(file)
                    config_data_list.append(config_data)
                    # save for global use
                    config_data_list_global[url] = config_data
        
    return config_data_list

def all_config_initial():
    '''
        # Introduction
        Read all config files and restore it in the memory
    '''
    global config_data_list_global
    for url_list in config_file_urls:
        for url in url_list:
            config_data = find_config_by_file_url(url)
            if config_data == None:
                with open(url,'r') as file:
                    config_data = yaml.safe_load(file)
                    # save for global use
                    config_data_list_global['url'] = config_data

def config_update(config_data):
    '''
        # Introduction
        Update the global config data by config_data
        
        # Param
        - config_data: The new data to updated to the configuration file
    '''
    global config_data_list_global
    logging_operation.write_log("The updating config data is "+ str(config_data), source = __name__, level = 1)
    logging_operation.write_log("The global config data is "+ str(config_data_list_global), source = __name__, level = 1)

    for item in config_data_list_global.items():
        # logging_operation.write_log(item, source = __name__, level = 1)
        if item[1]['config_name'] == config_data['config_name']:
            config_file_url = item[0]
            # update global data
            config_data_list_global[config_file_url] = config_data
            logging_operation.write_log("Updating successfully. /nThe updating config data is "+ str(config_data), source = __name__, level = 1)
            break
        
    return
