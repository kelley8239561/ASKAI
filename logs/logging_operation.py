import os,time
import logging, threading

# Handler
file_log_handler : logging.FileHandler # logfile
console_log_handler : logging.StreamHandler # console print
level_to_console = 0 # output min level
level_to_file = 10 # minimal output  level

# log file url
log_file_url = "logs/log_ASKAI.log"
# Handler initial
file_log_handler = logging.FileHandler(log_file_url) # logfile
file_log_handler.setLevel(0)
console_log_handler = logging.StreamHandler() # console print
console_log_handler.setLevel(0)
# Formater
log_formater = logging.Formatter("%(asctime)s - %(levelname)s - %(process)d - %(thread)d - %(name)s - \n%(message)s\n")
# Add Formater to Handler
file_log_handler.setFormatter(log_formater)
console_log_handler.setFormatter(log_formater)

def initial_log_config():
    '''
        # Introduction
        Initial Handler and Formater for global logs
    '''
    pass

def write_log(log_content:str, source:str = "__main__", level:int = 10):
    '''
        # Introduction:
        Write a str entity to log file
        
        # Param:
        - log_content: str
            The content to log
        - source: str
            The call file, normally the '__name__' of the calling position
        - style: str
            The usage environment of the log_content, 'debug' or 'run'
            - debug: for developing usage
            - run: for online usage
        - level: str
            The level of the log_content
            https://docs.python.org/zh-cn/3/library/logging.html#logging-levels
            - NOSET: value 0
            - DEBUG: value 10
            - INFOR: value 20
            - WARNING: value 30
            - ERROR: value 40
            - CRITICAL: value 50
    '''
    logger = logging.getLogger(source)
    logger.setLevel(level)
    logger.addHandler(file_log_handler)
    logger.addHandler(console_log_handler)
    logger.log(
        level,
        log_content, 
    )
    
def clean_log_file(begin_row:int = None, end_row:int = None):
    '''
        # Introduction
        Delete the logs records between begin_row and end_row
        
        # Params
        - begin_row: The clean operation begin from here. None equals 0 and 0 equals first.
        - end_row: The clean operation end here. None equals the end.
    '''
    global log_file_url
    with open(log_file_url,'r') as f:
        log_data = f.readlines()
        # write_log("logging lenth is " + str(log_data.__len__()),__name__,1)
    if not begin_row:
        begin_row = 0
    if not end_row:
        end_row = log_data.__len__()
    log_data_new = log_data[:begin_row] + log_data[end_row:]
    # write_log("logging lenth after cleaning is " + str(log_data_new.__len__()),__name__,1)
    
    with open(log_file_url,'w') as f:  
        f.writelines(log_data_new)

def auto_clean_log_file_by_time(**args):
    '''
        # Introduction
        AutoDelete logs as configurations or commands
    '''
    pass
 
# initialization
initial_log_config()