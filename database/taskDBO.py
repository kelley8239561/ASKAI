"""
_summary_
sqlite3

"""

import os
import sqlite3
from sqlite3 import Cursor,Connection
import threading
from task import taskClass

def initial():
    database = 'asset/tasks/Task.db'
    table = '''tasks (id INTEGER PRIMARY KEY, name TEXT, status INTEGER, instructions TEXT, objectives TEXT)'''
    conn = createConnection(database)
    # 初始化表
    createTable(conn,table)

def createConnection(database):
    """ 创建数据库连接 """
    conn = None
    try:
        conn = sqlite3.connect(database)
        print(os.getpid(),threading.current_thread().ident,'db connection success' )
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def createTable(conn:Connection,table):
    """ 创建表 """
    try:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS "+table)
    except sqlite3.Error as e:
        print(e)

def insert(conn:Connection, task):
    """ 插入 """
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", task)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def update(conn:Connection, task):
    """ 更新 """
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET name = ?, status = ?, instructions = ?, objectives = ? WHERE id = ?", task.getParam('name'),task.getParam('status'),task.getParam('taskInstruction'),task.getParam('objective'),task.getParam('id'))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def delete(conn:Connection, task):
    """ 删除用户 """
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE name = ?", (name,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def selectAll(conn:Connection):
    """ 查询所有任务 """
    resultList = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        for taskRow in cursor.fetchall():
            task = taskClass.OriginTask(taskRow)
            resultList.append(task)
        print(os.getpid(),threading.current_thread().ident,'selectAll result is:',resultList.__len__())
        return resultList
    except sqlite3.Error as e:
        print(e)
        
def update(conn:Connection,task):
    
    pass

