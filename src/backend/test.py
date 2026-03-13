import os
from pathlib import Path
import re
import time as _time
import pythoncom
from pywinauto import mouse
from pywinauto import Desktop

# from pyweixin.WeChatTools import Tools,Navigator


# from pywechat.WechatTools import Tools

# from pywechat.WechatAuto import get_groups_info,WechatSettings
from pywinauto.timings import Timings

from auto.WeChatBot import WeChatBot
from auto.WeChatToolsExt import ToolsExt,NavigatorExt
from auto.WeChatAutoExt import ContactsExt,MessagesExt, FriendSettingsExt
from auto.UielementsExt import (CustomsExt, GroupsExt, Login_window,Main_window,SideBar,Independent_window,Buttons,Texts,Menus,TabItems,MenuItems,Edits,Windows, WindowsExt,)

# Buttons=Buttons()#微信内部Button类型UI
Main_window=Main_window()#微信内部Window类型UI
Window=Windows()#微信内部Window类型UI
WindowsExt=WindowsExt()#微信内部Window类型UI
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
# groups = ContactsExt.get_recent_groups()
# for group in groups:
#     print(group[0])
#     print(group[1])

# from auto.pyweixin.utils import scan_for_new_messages,get_new_message_num
from auto.WeChatBot import WeChatBot
not_care={'session_item_服务号','session_item_公众号','session_item_QQ邮箱提醒','session_item_微信支付'}
# print(MessagesExt.check_new_messages())
# print(scan_for_new_messages(close_weixin=False))
# print(get_new_message_num(close_weixin=False))
# print(MessagesExt.dump_sessions())
# print(MessagesExt.dump_recent_sessions('Today'))
# print(WeChatBot.scan_for_new_messages(close_weixin=False))
# print(WeChatBot.pull_messages(friend='箭冠网络科技、京兆瓦肆',myname='albertyanm',number=10))
print("*" * 30)
CustomsExt=CustomsExt()
GroupsExt=GroupsExt()
t1 = _time.monotonic()
contact_list,main_window=NavigatorExt.open_contacts(is_maximize=False)
t2=_time.monotonic()
print(t2-t1)
contact_custom=main_window.child_window(**CustomsExt.AddNewFriendCustom)
# print(contact_custom.print_control_identifiers())
#企业微信联系人分区
ToolsExt.collapse_contacts(main_window,contact_list)
t3=_time.monotonic()
print(t3-t2)
new_friend_item=main_window.child_window(control_type='ListItem',title=r'新的朋友',class_name="mmui::ContactsCellGroupView")

# contact_item=main_window.child_window(control_type='ListItem',title_re=r'新的朋友\d+',class_name="mmui::ContactsCellGroupView")
if new_friend_item.exists(timeout=0.1):
    new_friend_item.click_input()


#切换到联系人分区内的第一个好友
def switch_to_first_friend(contact_list,contact_item):
    contact_list.type_keys('{HOME}')
    items=contact_list.children(control_type='ListItem')
    for i in range(len(items)):
        if items[i]==contact_item and i<len(items)-1:
            first_friend=i+1
            if items[i+1].window_text()=='':
                first_friend+=1
            break
    items[first_friend].click_input()    
switch_to_first_friend(contact_list,new_friend_item)
# if new_friend_item.children(control_type='ListItem'):
#     initial_message=new_friend_item.children(control_type='ListItem')[0]#刚打开聊天界面时的最后一条消息的listitem
#     initial_message.click_input()
#右侧自定义面板下的好友信息所在面板
a={'title':'','control_type':'Button','class_name':'mmui::ContactHeadView'}
b={'title':'','control_type':'Group','class_name':'mmui::XView'}
# new_friend_profile=contact_custom.child_window(**b)[-1]
# print(new_friend_profile.print_control_identifiers())
# if new_friend_profile:
#     print(new_friend_profile.element_info)
#     wxNum = new_friend_profile.descendants(control_type='Button',class_name='mmui::ContactHeadView')
#     if not wxNum:
#         for s in wxNum:
#             print(s)
#     print("好友信息面板已打开")
# else:
#     print("好友信息面板未打开")

# tn=_time.monotonic()
# print(tn-t1)
# 来源
source = contact_custom.child_window(auto_id='profile_pair_line.reader_hover_stacked_view_.reader_text_button_h_view.reader_text_button_stacked_view.value_reader_',class_name='mmui::ContactProfileTextView',control_type='Text')
# 昵称
name = contact_custom.child_window(auto_id='TextViewCanCopy',class_name="mmui::TextViewCanCopy", control_type="Text")
# 前往验证按钮
button = contact_custom.child_window(title="前往验证",class_name="mmui::XOutlineButton", control_type="Button")

if name:
    print(name.window_text())
if source:
    print(source.window_text())

if button:
    button.click_input()
    moments_window=ToolsExt.move_window_to_center(Window=WindowsExt.NewFriendVerifyFriendWindow)

def find_go_verify_button_by_descendants(contact_custom):
    """
    用 descendants 查找“前往验证”按钮

    为什么用 descendants：有些 Qt/UIA 控件层级不稳定，直接 child_window 可能偶发找不到，用遍历更抗层级变化。
    """
    candidates = contact_custom.descendants(title="前往验证", control_type="Button")
    return candidates[0] if candidates else None

# btn = find_go_verify_button_by_descendants(contact_custom)
# if btn:
#     print(btn.element_info)
#     # btn.click_input()
# else:
#     print("未找到：前往验证")
# contacts_button=main_window.child_window(**SideBar.Contacts)
#左上角微信按钮的红色消息提示(\d+条新消息)在FullDescription属性中,
#只能通过id来获取,id是30159，之前是30007,可能是qt组件映射关系不一样
# full_desc=contacts_button.element_info.element.GetCurrentPropertyValue(30159)
# print(full_desc)
# new_message_num=re.search(r'\d+',full_desc)#正则提取数量
# print(new_message_num.group(0))
#微信会话列表内ListItem标准格式:备注\s(已置顶)\s(\d+)条未读\s最后一条消息内容\s时间
# new_message_pattern=re.compile(r'\n\[(\d+)条\]')#只给数量分组.group(1)获取
# print(new_message_pattern)
# print(ToolsExt.where_weixin())
# FriendSettingsExt.change_remark('张建坤','张建坤1')
# print(MessagesExt.dump_recent_sessions('Today'))

# from pyweixin.WeChatAuto import Messages
# Messages.check_new_messages(search_pages=0)
# from utils.common_util import get_machine_code
# if __name__ == "__main__":
#     print(get_machine_code())
# from service.monitor_service import monitor_service
# monitor_service.start_monitor()



# def get_message_sender(listitem:ListItemWrapper,chat_list_rect,friend:str)->str:
#     '''
#     判断消息发送者
#     Args:
#         listitem: 消息列表项
#         chat_list_rect: 聊天列表的矩形区域
#     Returns:
#         'Self': 自己发送
#         'Other': 他人发送
#     '''
#     try:
#         item_rect = listitem.rectangle()
#         item_center_x = item_rect.mid_point().x
#         item_width = item_rect.width()
        
#         # 广度优先遍历寻找非满宽的内容元素
#         queue = [listitem]
#         content_rects = []
        
#         # 设置最大循环次数防止死循环
#         loop_count = 0
#         while queue and loop_count < 50:
#             loop_count += 1
#             curr = queue.pop(0)
#             try:
#                 children = curr.children()
#             except Exception:
#                 continue
                
#             for child in children:
#                 try:
#                     rect = child.rectangle()
#                     # 放宽阈值到 0.95，排除满宽容器
#                     if rect.width() < item_width * 0.95:
#                         content_rects.append(rect)
#                     else:
#                         # 满宽组件，继续深入查找
#                         queue.append(child)
#                 except Exception:
#                     continue
            
#             if len(content_rects) >= 2:
#                 break
        
#         # 如果找到几何特征，使用几何判断
#         if content_rects:
#             print("2222222222222222222222222222222")
#             avg_mid_x = sum(r.mid_point().x for r in content_rects) / len(content_rects)
#             if avg_mid_x < item_center_x:
#                 return friend
#             else:
#                 return 'albertyanm1'

#         # 如果没有找到非满宽元素，尝试【颜色判断】
#         try:
#             # 截取 ListItem 区域 (left, top, width, height)
#             region = (item_rect.left, item_rect.top, item_rect.width(), item_rect.height())
#             # 确保区域有效
#             if region[2] > 0 and region[3] > 0:
#                 img = pyautogui.screenshot(region=region)
#                 width, height = img.size
#                 pixels = img.load()
#                 mid_y = height // 2
                
#                 # 1. 从右向左扫描寻找绿色气泡 (自己)
#                 # 微信绿色气泡典型值 (149, 236, 105)
#                 for x in range(width - 10, width // 2, -5):
#                     if x < width:
#                         r, g, b = pixels[x, mid_y]
#                         # 绿色判定：G 分量显著大于 R 和 B
#                         if g > 180 and g > r + 20 and g > b + 20:
#                             return 'albertyanm2'
                            
#                 # 2. 从左向右扫描寻找非背景色 (他人)
#                 # 背景色通常为浅灰 (245, 245, 245) 或白色
#                 for x in range(10, width // 2, 5):
#                     if x < width:
#                         r, g, b = pixels[x, mid_y]
#                         # 如果不是背景色 (允许一定误差)
#                         is_background = (r > 240 and g > 240 and b > 240)
#                         if not is_background:
#                             # 且不是绿色 (再次确认)
#                             if not (g > 180 and g > r + 20 and g > b + 20):
#                                 return friend
#         except Exception as e:
#             print(f"Color check error: {e}")
#         print("3333333333333333333333")
#         # 最后的回退策略：位置判断
#         if chat_list_rect:
#             if item_rect.mid_point().x < chat_list_rect.mid_point().x:
#                 return friend
#             else:
#                 return 'albertyanm3'
            
#         return ''
            
#     except Exception:
#         return ''
    