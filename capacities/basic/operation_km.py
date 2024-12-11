import keyboard
from services import (
    service_main
)
from logs import logging_operation

def initial_hotkeys():
    '''
        # Introduction
        The default hotkeys to listen
    '''
    # ctrl+alt+q, quit the service_main
    keyboard.add_hotkey("ctrl+alt+q", callback = service_main.service_main_quit)
    logging_operation.write_log("Initial hotkeys.", source = __name__, level = 1)
    