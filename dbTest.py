from database import taskDBO

'''
db.initial()
for task in db.selectAll(db.createConnection('asset/tasks/Task.db')):
    print(task)
'''

conn = taskDBO.createConnection('asset/tasks/Task.db')

items = taskDBO.selectAll(conn)
print(items)