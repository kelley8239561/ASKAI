from services import service_main
from logs import logging_operation

if __name__ == '__main__':
    logging_operation.clean_log_file() # For Debug
    logging_operation.write_log("Welcome to ASKAI", source = __name__, level = 50)
    # main service
    service_main.main()
    logging_operation.write_log("Goodbye!", source = __name__, level = 1)