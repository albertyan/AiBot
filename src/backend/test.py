from pywechat.WechatTools import Tools
from pywechat.Uielements import (Login_window,Main_window,SideBar,Independent_window,Buttons,Texts,Menus,TabItems,MenuItems,Edits,Windows)
from pywechat.WechatAuto import get_groups_info,WechatSettings


Buttons=Buttons()#微信内部Button类型UI
Windows=Windows()#微信内部Window类型UI


# my = main_window.child_window(**Buttons.MySelfButton)
# my.click_input()  # 点击我的按钮
# print(f"2222: {my.window_text()}")  # 获取我的按钮的文本
# name = main_window.window(**Windows.ContactProfileWindow).texts()
# main_window.window(**Windows.ContactProfileWindow).print_control_identifiers()
# print(main_window.window(**Windows.ContactProfileWindow).Static3.window_text())  # 获取个人信息窗口的文本
# print(f"1111: {name}")
# myname=my.window_text()
# print(f"当前登录用户: {myname}")

# Tools.open_contacts_settings(is_maximize=False)


# from pywechat.WechatAuto import *
# from pywechat.Clock import schedule
# import threading
# import json
# def task():
#     print("任务执行中...")  # 替换为你的方法
#     threading.Timer(30, task).start()  # 60秒后再次启动
#     msg = check_new_message()
#     print(msg)
#     if msg != '未查找到新消息' :
#         for m in json.loads(msg):
#             AI_auto_reply_to_friend1(m)

# threading.Timer(0, task).start()
ContactProfileWindow={'class_name':'ContactProfileWnd','control_type':'Pane'}  #设置好友权限窗口

if __name__ == "__main__":
    # print(get_groups_info())
    main_window=Tools.open_wechat(is_maximize=False)
    myname=main_window.child_window(**Buttons.MySelfButton).window_text()
    print(f"当前登录用户: {myname}")  # 获取当前登录用户的名称
    my = main_window.child_window(**Buttons.MySelfButton)
    my.click_input()  # 点击我的按钮
    print(main_window.window(**ContactProfileWindow).Static3.window_text()) 
    # print(check_new_message())
    # my.click_input()
    WechatSettings.Auto_convert_voice_messages_to_text('open',is_maximize=False)

