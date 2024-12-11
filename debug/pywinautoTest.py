from task.prompts import taskPrompts
from pywinauto.application import Application
from pywinauto import Desktop

'''
app = Application(backend='uia').start(r'D:\WX\WeChat\WeChat.exe')
dlg = app.window(title='微信')
loginButton = dlg.child_window(title='扫码登录')
loginButton.draw_outline(colour='green') 
loginButton.click_input()
'''

apps = Desktop().windows()
for app in apps:
    print(type(app),app)