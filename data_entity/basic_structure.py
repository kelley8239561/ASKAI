from enum import Enum,auto

class Message_Source(Enum):
    '''
        # Introduction
        Where the message come from
        
        # Values
        - WECHAT = 1
        - CHATBOX = 2
        - MAIL = 3
        - WINDOWS_MIC = 4
        - WEARABLE_MIC = 5 
    '''
    WECHAT = auto()
    CHATBOX = auto()
    MAIL = auto()
    WINDOWS_MIC = auto()
    WEARABLE_MIC = auto()


