import inspect,sqlite3
import data_entity.basic_structure
from datetime import datetime
import data_entity.message
from logs import logging_operation

# Attribute type mapping
db_to_python_type_mapping = {
    str:'TEXT',
    int:'INTEGER',
    dict:'TEXT',
    datetime:'timestamp',
    float:'REAL',
    data_entity.basic_structure.Message_Source:'message_source',
}

# 
def type_mapping_initial():
    sqlite3.register_adapter(data_entity.basic_structure.Message_Source,adapt_Message_Source)
    sqlite3.register_converter('message_source',convert_Message_Source)

# mapping Message_Source - INTEGER
def adapt_Message_Source(message_source:data_entity.basic_structure.Message_Source):
    return message_source.value

def convert_Message_Source(message_source_value):
    return data_entity.basic_structure.Message_Source(int(message_source_value))