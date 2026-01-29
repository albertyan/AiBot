import os
from pathlib import Path
import time
from pywinauto import mouse
from pywinauto import Desktop

# from pyweixin.WeChatTools import Tools,Navigator


# from pywechat.WechatTools import Tools
from pyweixin.Uielements import (Login_window,Main_window,SideBar,Independent_window,Buttons,Texts,Menus,TabItems,MenuItems,Edits,Windows)
# from pywechat.WechatAuto import get_groups_info,WechatSettings
from pywinauto.timings import Timings
from pyweixin.WeChatAuto import Contacts

from auto.WeChatToolsExt import ToolsExt,NavigatorExt
from auto.WeChatAutoExt import ContactsExt

# Buttons=Buttons()#微信内部Button类型UI
Main_window=Main_window()#微信内部Window类型UI
Window=Windows()#微信内部Window类型UI
SideBar=SideBar()#主界面左侧的侧边栏
Timings.slow()
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
# ContactProfileWindow={'class_name':'ContactProfileWnd','control_type':'Pane'}  #设置好友权限窗口

# if __name__ == "__main__":
#     # print(get_groups_info())
#     main_window=Tools.open_wechat(is_maximize=False)
#     myname=main_window.child_window(**Buttons.MySelfButton).window_text()
#     print(f"当前登录用户: {myname}")  # 获取当前登录用户的名称
#     my = main_window.child_window(**Buttons.MySelfButton)
#     my.click_input()  # 点击我的按钮
#     print(main_window.window(**ContactProfileWindow).Static3.window_text()) 
#     # print(check_new_message())
#     # my.click_input()
#     WechatSettings.Auto_convert_voice_messages_to_text('open',is_maximize=False)
# desktop=Desktop(backend='uia')#Window桌面
# # main_window=desktop.window(**Main_window.MainWindow)
# main_window= NavigatorExt.open_weixin()
# ToolsExt.cancel_pin(main_window)
# # 检查微信是否运行
# is_running = ToolsExt.is_weixin_running()
# print(f"微信是否运行中: {is_running}")
# if not is_running:
#     print("微信未运行，请先启动微信")
#     exit()
# print("1" + "-" * 20 + time.strftime("%H:%M:%S", time.localtime()))
# # 等待窗口出现
# if not main_window.exists(timeout=0.1):
#     print("未找到微信主窗口，请确保已登录并打开主界面")
#     exit()
# # main_window.set_focus()
# print("2" + "-" * 20 + time.strftime("%H:%M:%S", time.localtime()))
# # 恢复窗口状态（如果最小化）
# try:
#     if main_window.get_show_state() == 2: # 2 代表最小化
#         main_window.restore()
#     main_window.set_focus()
# except Exception as e:
#     print(f"窗口操作异常: {e}")
# print("3" + "-" * 20 + time.strftime("%H:%M:%S", time.localtime()))
# # 获取窗口对象和坐标
# main = main_window.wrapper_object()
# print("4" + "-" * 20 + time.strftime("%H:%M:%S", time.localtime()))
# rect = main.rectangle()
# print(f"窗口坐标范围: {rect}")
# #print(f"窗口左上角坐标: ({rect.left}, {rect.top})")
# # 计算相对坐标
# left = rect.left + 33
# top = rect.top + 55
# print(f"鼠标将移动到: ({left}, {top})")
# # 移动鼠标
# # mouse.move()
# mouse.click(coords=(left, top)) # 暂时注释，防止误操作
# print("5" + "-" * 20 + time.strftime("%H:%M:%S", time.localtime()))
# text = {'control_type':'Text','class_name':'mmui::ContactProfileTextView'}


# # my = Tools.move_window_to_center(Window.PopUpProfileWindow)       
# # time.sleep(1)
# # handle=desktop.window(**Window.PopUpProfileWindow).handle
# # print(handle)
# # win32gui.ShowWindow(handle,1)
# # my=desktop.window(handle=handle)

# time.sleep(0.01)
# # my=desktop.window(**Window.PopUpProfileWindow)
# my=NavigatorExt.find_my_info_window()
# try:
#     my.wait('exists', timeout=2) # 等待窗口出现，避免 ElementNotFoundError
#     print("好友信息窗口已打开")
# except Exception:
#     print("好友信息窗口未打开(超时)")

# # if my.exists(timeout=0.1):
# #     print("好友信息窗口已打开")
# # else:
# #     print("好友信息窗口未打开")

# # my.print_control_identifiers()
# print("6" + "-" * 20 + time.strftime("%H:%M:%S", time.localtime()))
# # 使用 child_window 配合 found_index 快速获取，避免遍历整个树
# try:
#     # 尝试获取第一个匹配的控件
#     no = my.child_window(found_index=0, **text).window_text()
# except Exception:
#     no = "未找到"
# print(f"当前好友号码: {no}")
# print("7" + "-" * 20 + time.strftime("%H:%M:%S", time.localtime()))

# main_window.set_focus()

# friends = ContactsExt.get_friends_detail()

# for friend in friends:
#     print(friend + ",")
# info={'昵称':nickname,'微信号':wx_number,'地区':region,'备注':remark,'电话':phonenumber,
# '标签':tag,'描述':descrption,'朋友权限':permission,'共同群聊':f'{common_group_num}','个性签名':signature,'来源':source}
groups = ContactsExt.get_recent_groups()
for group in groups:
    print(group)
