import re
import time

import pyautogui
from loguru import logger

from warnings import warn
from pywinauto import WindowSpecification
from pywinauto.controls.uia_controls import ListItemWrapper,ListViewWrapper
from auto.pyweixin.Config import GlobalConfig
from auto.pyweixin.Uielements import Main_window, SideBar, Lists,Independent_window,Buttons,Edits
from auto.pyweixin.WeChatTools import Navigator,Tools
from auto.pyweixin.Warnings import NoChatHistoryWarning
import win32gui
from pywinauto import mouse,Desktop

from auto.pyweixin.Errors import NoSuchFriendError

Main_window=Main_window()#主界面UI
SideBar=SideBar()#侧边栏UI
# Buttons=Buttons()#所有Button类型UI
Edits=Edits()#所有Edit类型UI
Lists=Lists()#所有List类型UI
# Windows=Windows()#所有Windows类型UI
Independent_window=Independent_window()#独立主界面UI
desktop=Desktop(backend='uia')#Window桌面
pyautogui.FAILSAFE=False#防止鼠标在屏幕边缘处造成的误触

#正则匹配获取时间
timestamp_pattern=re.compile(r'(?<=\s)(\d{4}/\d{1,2}/\d{1,2}|\d{1,2}/\d{1,2}|\d{2}:\d{2}|昨天 \d{2}:\d{2}|星期\w)$')#主界面左侧会话列表内的时间戳
#获取最后一条消息内容
def get_latest_message(listitem):
    name=listitem.automation_id().replace('session_item_','')
    res=listitem.window_text().replace(name,'')
    msg=timestamp_pattern.sub(repl='',string=res).replace('已置顶 ','').replace('消息免打扰','')
    return msg

def get_sending_time(listitem):
    timestamp=timestamp_pattern.search(listitem.window_text().replace('消息免打扰 ',''))
    if timestamp:
        return timestamp.group(0)
    else:
        return ''
#根据recent筛选和过滤会话
def filter_sessions(ListItems,recent:str='Today'):
    lastyear=str(int(time.strftime('%y'))-1)+'/'#去年
    thismonth=str(int(time.strftime('%m')))+'/'#去年
    ListItems=[ListItem for ListItem in ListItems if get_sending_time(ListItem)]
    if recent=='Year' or recent=='Month':
        ListItems=[ListItem for ListItem in ListItems if lastyear not in get_sending_time(ListItem)]
    if recent=='Week':
        ListItems=[ListItem for ListItem in ListItems if '/' not in get_sending_time(ListItem)]
    if recent=='Today' or recent=='Yesterday':
        ListItems=[ListItem for ListItem in ListItems if ':' in get_sending_time(ListItem)]
    # if chat_only:
    #     ListItems=[ListItem for ListItem in ListItems if get_latest_message(ListItem)!='']
    return ListItems

class WeChatBot:

    def __init__(self):
        pass

    @staticmethod
    def pull_messages(friend:str,myname:str,number:int,search_pages:int=None,is_maximize:bool=None,close_weixin:bool=None,main_window:WindowSpecification=None)->list[str]:
        '''
        该函数用来从聊天界面获取聊天消息,也可当做获取聊天记录
        Args:
            friend:好友名称
            myname:自己的名称
            number:获取的消息数量
            search_pages:打开好友聊天窗口时在会话列表中查找好友时滚动列表的次数,默认为5,一次可查询5-12人,为0时,直接从顶部搜索栏搜索好友信息打开聊天界
            is_maximize:微信界面是否全屏，默认不全屏
            close_weixin:任务结束后是否关闭微信，默认关闭
        Returns:
            messages:聊天记录中的消息(时间顺序从晚到早)
        '''
        def get_message_sender(listitem:ListItemWrapper,friend:str, myname:str='albertyanm')->str:
            '''
            判断消息发送者
            Args:
                listitem: 消息列表项
            Returns:
                'Self': 自己发送
                'Other': 他人发送
            '''
            try:
                item_rect = listitem.rectangle()
                # 如果没有找到非满宽元素，尝试【颜色判断】
                try:
                    # 截取 ListItem 区域 (left, top, width, height)
                    region = (item_rect.left, item_rect.top, item_rect.width(), item_rect.height())
                    # 确保区域有效
                    if region[2] > 0 and region[3] > 0:
                        img = pyautogui.screenshot(region=region)
                        width, height = img.size
                        pixels = img.load()
                        mid_y = height // 2
                        # 1. 从右向左扫描寻找绿色气泡 (自己)
                        # 微信绿色气泡典型值 (149, 236, 105)
                        for x in range(width - 10, width // 2, -5):
                            if x < width:
                                r, g, b = pixels[x, mid_y]
                                # 绿色判定：G 分量显著大于 R 和 B
                                if g > 180 and g > r + 20 and g > b + 20:
                                    return 'Self'
                                    
                        # 2. 从左向右扫描寻找非背景色 (他人)
                        # 背景色通常为浅灰 (245, 245, 245) 或白色
                        for x in range(10, width // 2, 5):
                            if x < width:
                                r, g, b = pixels[x, mid_y]
                                # 如果不是背景色 (允许一定误差)
                                is_background = (r > 240 and g > 240 and b > 240)
                                if not is_background:
                                    # 且不是绿色 (再次确认)
                                    if not (g > 180 and g > r + 20 and g > b + 20):
                                        return friend
                except Exception as e:
                    print(f"Color check error: {e}")
                return ''
            except Exception:
                return ''
        
        if is_maximize is None:
            is_maximize=GlobalConfig.is_maximize
        if close_weixin is None:
            close_weixin=GlobalConfig.close_weixin
        if search_pages is None:
            search_pages=GlobalConfig.search_pages
        messages=[]
        sender=[]
        messages_dict = list(zip(sender,messages))
        main_window=Navigator.open_dialog_window(friend=friend,is_maximize=is_maximize,search_pages=search_pages)
        # main_window=WeChatBot.find_friend_window(friend,main_window)
        chat_list=main_window.child_window(**Lists.FriendChatList)
        if not chat_list.exists(timeout=0.1):
            print(f'非正常好友或群聊,无法获取聊天信息！')
            return messages
        else:
            if not chat_list.children(control_type='ListItem'):
                warn(message=f'你与{friend}的聊天记录为空,无法获取聊天信息',category=NoChatHistoryWarning)
                return messages
            last_item=chat_list.children(control_type='ListItem')[-1]
            messages.append(last_item.window_text())
            sender.append(get_message_sender(last_item,friend,myname))
            logger.debug("pull_messages 3 :" + time.strftime("%Y-%m-%d %H:%M:%S" ,time.localtime()))
            # Tools.activate_chatList(chat_list)
            while len(messages)<number:
                chat_list.type_keys('{UP}')
                selected=[listitem for listitem in chat_list.children(control_type='ListItem') if listitem.has_keyboard_focus()]
                if selected and selected[0].class_name()!='mmui::ChatItemView':
                    messages.append(selected[0].window_text())
                    sender.append(get_message_sender(selected[0],friend,myname))
                if not selected:
                    break
            logger.debug("pull_messages 4 :" + time.strftime("%Y-%m-%d %H:%M:%S" ,time.localtime()))
            chat_list.type_keys('{END}')
            messages=messages[-number:]
            sender=sender[-number:]
            if close_weixin:
                main_window.close()

            messages_dict = list(zip(sender,messages))
        return messages_dict
            
    @staticmethod
    def scan_for_new_messages(main_window:WindowSpecification=None,delay:float=0.3)->dict:
        '''
        该函数用来扫描检查一遍会话列表中的所有新消息,返回发送对象以及新消息数量(不包括免打扰)
        Args:
            main_window:微信主界面实例,可以用于二次开发中直接传入main_window,也可以不传入,不传入自动打开
            delay:在会话列表查询新消息时的翻页延迟时间,默认0.3秒
        Returns:
            newMessages_dict:有新消息的好友备注及其对应的新消息数量构成的字典
        '''

        # (修改原因：仅增加调试日志，不修改原有逻辑)
        logger.debug("Entering scan_for_new_messages")
        def traverse_messsage_list(listItems):
            #newMessageTips为newMessagefriends中每个元素的文本:['测试365 5条新消息','一家人已置顶20条新消息']这样的字符串列表
            listItems=[listItem for listItem in listItems if listItem.automation_id() not in not_care 
            and '消息免打扰' not in listItem.window_text()]
            listItems=[listItem for listItem in listItems if new_message_pattern.search(listItem.window_text())]
            senders=[listItem.automation_id().replace('session_item_','') for listItem in listItems]
            newMessageTips=[listItem.window_text() for listItem in listItems if listItem.window_text() not in newMessageSenders]
            newMessageNum=[int(new_message_pattern.search(text).group(1)) for text in newMessageTips]
            logger.debug(f"traverse_messsage_list found {len(senders)} items. Senders: {senders}, Nums: {newMessageNum}")
            return senders,newMessageNum,newMessageTips

        not_care={'session_item_服务号','session_item_公众号'}
        if main_window is None:
            # main_window=Navigator.open_weixin(is_maximize=False)
            main_window=WeChatBot.find_window()
            logger.debug("scan_for_new_messages: main_window opened.")
        newMessageSenders=[]
        newMessageTipList=[]
        newMessages_dict=dict(zip(newMessageSenders,newMessageTipList))
        chats_button=main_window.child_window(**SideBar.Chats)
        #左上角微信按钮的红色消息提示(\d+条新消息)在FullDescription属性中,
        #只能通过id来获取,id是30159，之前是30007,可能是qt组件映射关系不一样
        full_desc=chats_button.element_info.element.GetCurrentPropertyValue(30159)
        logger.debug(f"Full description property: {full_desc}")
        new_message_num=re.search(r'\d+',full_desc)#正则提取数量
        #微信会话列表内ListItem标准格式:备注\s(已置顶)\s(\d+)条未读\s最后一条消息内容\s时间
        new_message_pattern=re.compile(r'\n\[(\d+)条\]')#只给数量分组.group(1)获取
        if not new_message_num:
            print(f'没有新消息')
            logger.debug("No new messages found.")
            return {}
        if new_message_num:
            new_message_num=int(new_message_num.group(0))
            logger.debug(f"Total new messages to find: {new_message_num}")
            session_list=main_window.child_window(**Main_window.ConversationList)
            time.sleep(0.2)
            logger.debug(f"target={new_message_num}")
            #遍历获取带有新消息的ListItem
            listItems=session_list.children(control_type='ListItem')
            time.sleep(delay)
            senders,nums,newMessageTips=traverse_messsage_list(listItems)
            logger.debug(f"extracted: {len(senders)} senders. Nums: {nums}")
            ##提取姓名和数量
            newMessageSenders.extend(senders)
            newMessageTipList.extend(newMessageTips)
            newMessages_dict=dict(zip(newMessageSenders,newMessageTipList))
            not_={'QQ邮箱提醒','微信支付','微信游戏','服务通知'}
            newMessages_dict=[{sender:tip} for sender,tip in newMessages_dict.items() if sender not in not_]
        logger.debug(f"Scan finished. Returning: {newMessages_dict}")
        return newMessages_dict

    @staticmethod
    def find_window()->WindowSpecification:
        '''该方法用来将已打开的界面移动到屏幕中央并返回该窗口的windowspecification实例
        Args:
            Window:pywinauto定位元素kwargs参数字典
            Window_handle:窗口句柄
        '''
        # 这里使用 auto.pyweixin 是因为本项目将 pyweixin 作为 auto 的子包集成，
        # 直接 import pyweixin 在未安装独立 pyweixin 包的环境下会触发 ModuleNotFoundError
        from auto.pyweixin.WeChatTools import WxWindowManage
        wx=WxWindowManage()
        handle=wx.find_wx_window()
        desktop=Desktop(**Independent_window.Desktop)
        win32gui.ShowWindow(handle,1)
        window=desktop.window(handle=handle)
        window.restore()
        return window

    @staticmethod
    def find_friend_window(friend:str,main_window:WindowSpecification=None)->WindowSpecification:
        '''该方法用来查找好友窗口
        Args:
            friend_name:好友备注
        Returns:
            friend_window:好友窗口的windowspecification实例
        '''
        logger.debug(f"[find_friend_window] start friend={friend!r}")
        if main_window is None:
            main_window=WeChatBot.find_window()
        logger.debug("[find_friend_window] find_window ok")
        chat_button=main_window.child_window(**SideBar.Chats)
        #先看看当前聊天界面是不是好友的聊天界面
        current_chat=main_window.child_window(**Edits.CurrentChatEdit)
        logger.debug(f"[find_friend_window] current_chat element: {current_chat.element_info}")
        if current_chat.exists(timeout=0.2) and current_chat.window_text()==friend:
            logger.debug("[find_friend_window] current chat matched target, focusing edit area")
            edit_area=main_window.child_window(**Edits.CurrentChatEdit)
            if edit_area.exists(timeout=0.1) and edit_area.is_visible():
                edit_area.click_input()
            #如果当前主界面聊天界面顶部的名称为好友名称，直接返回结果
            return main_window
        else:#否则直接从顶部搜索栏出搜索结果
            logger.debug("[find_friend_window] current chat not matched, using search flow")
            #如果会话列表不存在或者不可见的话才点击一下聊天按钮
            chat_button.click_input()
            logger.debug("[find_friend_window] clicked chat button")
            # main_window = WeChatBot.find_window()
            
            search=main_window.descendants(**Main_window.Search)[0]
            logger.debug("[find_friend_window] descendants returned, about to read search.element_info")
            search.click_input()
            search.set_text(friend)
            logger.debug("[find_friend_window] search text set, waiting for results")
            time.sleep(0.5)
            search_results=main_window.child_window(title='',control_type='List')
            search_result=Tools.get_search_result(friend=friend,search_result=search_results)
            if search_result:
                logger.debug("[find_friend_window] search_result found, opening chat")
                search_result.click_input()
                edit_area=main_window.child_window(**Edits.CurrentChatEdit)
                if edit_area.exists(timeout=0.1):
                    edit_area.click_input()
                return main_window
            else:#搜索结果栏中没有关于传入参数friend好友昵称或备注的搜索结果，关闭主界面,引发NosuchFriend异常
                logger.debug("[find_friend_window] search_result not found, closing main_window and raising NoSuchFriendError")
                chat_button.click_input()
                main_window.close()
                raise NoSuchFriendError
