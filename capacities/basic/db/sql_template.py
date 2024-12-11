# sql template list
sql_instruction_list = {
    'get_tabel_list':"SELECT name FROM sqlite_master WHERE type='table'",
    'create_table':"CREATE TABLE {table_name}({column_list})",
    # column_list_str = 'message_id, sender', value_list_str = '? , ? , ?'
    'insert':"INSERT INTO {table_name} ({column_list_str}) VALUES ({value_list_str})",
    # column_name_list = "aaa, bbb, ccc"
    # condition_statement = "aaa = 1 and bbb = '111'"
    # order_column = "aaa, bbb ,ccc"
    # order = "ASC" / "DESC"
    'select':"SELECT {column_name_list} FROM {table_name} WHERE {condition_statement} ORDER BY {order_column_list} {order}",
    # column_list_str_to_update / column_list_str_to_find = 'name = ?, status = ?, instructions = ?, objectives = ? '
    'update':"UPDATE {table_name} SET {column_list_str_to_update} WHERE {column_list_str_to_find}",
    # column_list_str_to_find = '**_id = ? '
    'delete':"DELETE FROM {table_name} WHERE {column_list_str_to_find}",
}


