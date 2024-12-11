import inspect
from sqlite3 import Cursor,Connection,Error,connect
import traceback
import data_entity
import capacities.basic.db.tp_db
import data
import data_entity.basic_structure,data_entity.message,data_entity.basic_class
from accounts import admin_manager, login_manager
from logs import logging_operation
from capacities.basic.db import sql_template, tp_db
from capacities.basic.file import operation_file
tp_db
# database name and path
db_path = "data/"
db_name = login_manager.get_login_account() + "_ASKAI_local.db"

def initial(path:str = None, name:str = None):
    '''
        # Introduction
        Intial the database configuration
        # Params
        - path
        # Returns
    '''
    # Initial database url
    global db_path,db_name
    if path and name:
        db_path = path
        db_name = name
    try:
        # Initial database
        get_connection()
        
        # Initial attribute type mapping
        tp_db.type_mapping_initial()
        
        # Initial table
        table_initial()
        
    except Error as e:
        logging_operation.write_log(f"Database error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)

def table_initial():
    '''
        # Introduction
        Check if all tables have been created and create the tables which have not been created yet.
    '''
    # Get current table list from database
    temp_table_list = [table_tuple[0] for table_tuple in execute(sql_template.sql_instruction_list['get_tabel_list'])]
    logging_operation.write_log("The current tables are \n" + str(temp_table_list), source = __name__, level = 1)
    # check tables
    for entity in data_entity.entity_manager.get_entity_list_for_db_table():
        if not entity[0] in temp_table_list:
            create_table(entity[1])
     
def get_connection():
    '''
        # Introduction
        Get DB connection by db url
        # Returns
        - The database connection instance
    '''
    global db_path,db_name
    try:
        return connect(db_path + db_name)
    except Error as e:
        logging_operation.write_log(f"Database error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)

def execute(sql_instruction):
    '''
        # Introduction
        
        # Params
        
    '''
    con = get_connection()
    try:
        with con:
            cursor = get_connection().cursor()
            cursor.execute(sql_instruction)
            return cursor.fetchall()
    except Error as e:
        logging_operation.write_log(f"Database error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)

def create_table(data_entity_class:type):
    '''
        # Introduction
        Create a table according to the entity
        # Params
        - entity: a class defination
    '''
    con = get_connection()
    try:
        with con:
            cursor = con.cursor()
            table_name = data_entity_class.__name__.split('.')[-1]
            # column description structured list
            column_list = list()
            # column description string format
            column_list_str = ''
            logging_operation.write_log(f"Data entity attributes are \n{data_entity_class.get_attribute_annotition().items()}" , source = __name__, level = 50)
            if not len(attribute_annotition := data_entity_class.get_attribute_annotition()) == 0:
                for attribute in attribute_annotition.items():
                    column = (
                        attribute[0],
                        tp_db.db_to_python_type_mapping[attribute[1]],
                    )
                    column_str = f"{attribute[0]} {tp_db.db_to_python_type_mapping[attribute[1]]} "
                    # end with '_id', set the attribute PRIMARY KEY and AUTOINCREMENT
                    if attribute[0].endswith('_id'):
                        column = column + ('PRIMARY KEY AUTOINCREMENT',)
                        column_str = column_str + "PRIMARY KEY AUTOINCREMENT,"
                    else:
                        column = column + ('',)
                        column_str = column_str + ","
                    column_list.append(column)
                    column_list_str = column_list_str + column_str
                column_list_str = column_list_str[:-1] # Trim ','
                
                sql = sql_template.sql_instruction_list['create_table'].format(
                    table_name = table_name,
                    column_list = column_list_str,
                )
                logging_operation.write_log(f"sql is {sql}", source = __name__, level = 1)
                cursor.execute(sql)
            else:
                logging_operation.write_log(f"Class {data_entity_class} has no attribute, we can not create a table with no column(attribute)", source = __name__, level = 1)

    except Error as e:
        logging_operation.write_log(f"Database error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)

def insert(data_entity_list):
    '''
        # Introduction
        Insert data to the table according to the data_entity_list
        
        # Params
        - data_entity_list: list of entitied in data_entity
    '''
    con = get_connection()
    
    try:
        table_name = data_entity_list[0].__class__.__name__
        
        with con:
            data_list = []
            for data_entity in data_entity_list:  
                cursor = con.cursor()
                # column name and '?'
                column_list_str, value_list_str = '', ''
                # data
                data = tuple()
                data_entity_dict = data_entity.to_dict()
                for attribute in data_entity_dict.items():
                    column_list_str = column_list_str + f"{attribute[0]},"
                    value_list_str = value_list_str + f"?,"
                    data = data + (attribute[1],)
                if not column_list_str == '':
                    column_list_str = column_list_str[:-1]
                    value_list_str = value_list_str[:-1]
                # insert sql    
                sql = sql_template.sql_instruction_list['insert'].format(
                    table_name = table_name,
                    column_list_str = column_list_str,
                    value_list_str = value_list_str,
                )                
                data_list.append(data)
                logging_operation.write_log(f"Insert sql is \n{sql}\n{data}", source = __name__, level = 1)
            cursor.executemany(sql,data_list)
            con.commit()
    except Error as e:
        logging_operation.write_log(f"Database error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
    
def select(data_entity_class:type, column_name_list:list[str] = None, condition_statement = None, order_column_list = None, order = "ASC"):
    '''
        # Introduction
        Select data from database
        # Params
    '''
    con = get_connection()
    result_list = list()
    try:
        with con:
            cursor = con.cursor()
            # select column
            column_name_list_str = ""
            if column_name_list:
                for column_name in column_name_list:
                    column_name_list_str = f"{column_name_list_str},{column_name}"
                column_name_list_str = column_name_list_str[1:]
            else:
                column_name_list_str = '*'
            
            # table
            table_name = data_entity_class.__name__
            
            # condition
            if condition_statement:
                condition_statement_str = condition_statement
            else:
                condition_statement_str = True
            
            # order column and order
            order_column_list_str = ""
            if order_column_list:
                for column_name in order_column_list:
                    order_column_list_str = f"{order_column_list_str},{column_name}"
                column_name_list_str = column_name_list_str[1:]
            else:
                order_column_list_str = "NULL"
                order = ""
            
            sql = sql_template.sql_instruction_list['select'].format(
                    column_name_list = column_name_list_str,
                    table_name = table_name,
                    condition_statement = condition_statement_str,
                    order_column_list = order_column_list_str,
                    order = order
                )
            logging_operation.write_log(f"The select sql is \n{sql}", source = __name__, level = 1)

            cursor.execute(sql)
            result_list = cursor.fetchall()
            # result_list = data_entity.entity_normalization.data_list_to_entity_list(column_name_list,data_list,data_entity_class)
            
    except Error as e:
        logging_operation.write_log(f"Database error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
    
    return result_list

def update(origin_data_entity):
    '''
        # Introduction
        select data from database
        # Params
    '''
    
    con = get_connection()
    result = True
    try:
        with con:
            data = tuple()
            cursor = con.cursor()
            data_dict:dict = origin_data_entity.to_dict()
            # table_name
            table_name = origin_data_entity.__class__.__name__
            # column_list_str_to_update
            column_list_str_to_update = ""
            if not len(data_dict) == 0: 
                for data_item in data_dict.items():
                    # column_list_str_to_update = f"{column_list_str_to_update},{data_item[0]} = {data_item[1]}"
                    column_list_str_to_update = f"{column_list_str_to_update},{data_item[0]} = ?"
                    data = data + (data_item[1],)
                if not column_list_str_to_update == '':
                    column_list_str_to_update = column_list_str_to_update[1:]
            else:
                return False
            # column_list_str_to_find
            if not (primary_key_str:=origin_data_entity.primary_key()) == None:
                if  not (primary_key_value := data_dict.get(primary_key_str, "No keys")) == 'No keys':
                    # column_list_str_to_find = f"{primary_key_str} = {primary_key_value}"
                    column_list_str_to_find = f"{primary_key_str} = ?"
                    data = data + (primary_key_value,)
                else:
                    return False
            else:
                return False
            
            sql = sql_template.sql_instruction_list['update'].format(
                    table_name = table_name,
                    column_list_str_to_update = column_list_str_to_update,
                    column_list_str_to_find = column_list_str_to_find,
                )
            logging_operation.write_log(f"The update sql is \n{sql}", source = __name__, level = 1)
            cursor.execute(sql,data)
    except Error as e:
        logging_operation.write_log(f"Database error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
        return False
    return result

def delete(origin_data_entity):
    '''
        # Introduction
        delete data from database
        
        # Params
        - origin_data_entity: The relative entity of the row / rows about to delete
        
        # Returns
        - True 
    '''
    con = get_connection()
    result = True
    try:
        with con:
            data = tuple()
            cursor = con.cursor()
            data_dict:dict = origin_data_entity.to_dict()
            # table_name
            table_name = origin_data_entity.__class__.__name__
            
            # column_list_str_to_find
            if not (primary_key_str:=origin_data_entity.primary_key()) == None:
                if  not (primary_key_value := data_dict.get(primary_key_str, "No keys")) == 'No keys':
                    # column_list_str_to_find = f"{primary_key_str} = {primary_key_value}"
                    column_list_str_to_find = f"{primary_key_str} = ?"
                    data = data + (primary_key_value,)
                else:
                    return False
            else:
                return False
            
            sql = sql_template.sql_instruction_list['delete'].format(
                    table_name = table_name,
                    column_list_str_to_find = column_list_str_to_find,
                )
            logging_operation.write_log(f"The delete sql is \n{sql}", source = __name__, level = 1)
            cursor.execute(sql,data)
    except Error as e:
        logging_operation.write_log(f"Database error \n{e}\n{traceback.format_exc()}", source = __name__, level = 1)
        return False
    return result
    
    

