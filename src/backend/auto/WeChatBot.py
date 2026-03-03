from traitlets import Instance
import re
import time
from pywinauto import WindowSpecification
from auto.pyweixin.Config import GlobalConfig
from auto.pyweixin.Uielements import Main_window, SideBar
from auto.pyweixin.WeChatTools import Navigator

Main_window=Main_window()#主界面UI
SideBar=SideBar()#侧边栏UI
# Buttons=Buttons()#所有Button类型UI
# Edits=Edits()#所有Edit类型UI
# Lists=Lists()#所有List类型UI
# Windows=Windows()#所有Windows类型UI
# pyautogui.FAILSAFE=False#防止鼠标在屏幕边缘处造成的误触
# desktop=Desktop(backend='uia')


def scan_for_new_messages(main_window:WindowSpecification=None,delay:float=0.3,is_maximize:bool=None,close_weixin:bool=None)->dict:
    '''
    该函数用来扫描检查一遍会话列表中的所有新消息,返回发送对象以及新消息数量(不包括免打扰)
    Args:
        main_window:微信主界面实例,可以用于二次开发中直接传入main_window,也可以不传入,不传入自动打开
        delay:在会话列表查询新消息时的翻页延迟时间,默认0.3秒
        is_maximize:微信界面是否全屏，默认不全屏
        close_weixin:任务结束后是否关闭微信，默认关闭
    Returns:
        newMessages_dict:有新消息的好友备注及其对应的新消息数量构成的字典
    '''
    def traverse_messsage_list(listItems):
        #newMessageTips为newMessagefriends中每个元素的文本:['测试365 5条新消息','一家人已置顶20条新消息']这样的字符串列表
        listItems=[listItem for listItem in listItems if listItem.automation_id() not in not_care 
        and '消息免打扰' not in listItem.window_text()]
        listItems=[listItem for listItem in listItems if new_message_pattern.search(listItem.window_text())]
        senders=[listItem.automation_id().replace('session_item_','') for listItem in listItems]
        newMessageTips=[listItem.window_text() for listItem in listItems if listItem.window_text() not in newMessageSenders]
        newMessageNum=[int(new_message_pattern.search(text).group(1)) for text in newMessageTips]
        return senders,newMessageNum,newMessageTips

    not_care={'session_item_服务号','session_item_公众号'}
    if is_maximize is None:
        is_maximize=GlobalConfig.is_maximize
    if close_weixin is None:
        close_weixin=GlobalConfig.close_weixin
    if main_window is None:
        main_window=Navigator.open_weixin(is_maximize=is_maximize)
    newMessageSenders=[]
    newMessageNums=[]
    newMessageTipList=[]
    newMessages_dict=dict(zip(newMessageSenders,newMessageNums))
    chats_button=main_window.child_window(**SideBar.Chats)
    chats_button.click_input()
    #左上角微信按钮的红色消息提示(\d+条新消息)在FullDescription属性中,
    #只能通过id来获取,id是30159，之前是30007,可能是qt组件映射关系不一样
    full_desc=chats_button.element_info.element.GetCurrentPropertyValue(30159)
    message_list_pane=main_window.child_window(**Main_window.ConversationList)
    message_list_pane.type_keys('{HOME}')
    new_message_num=re.search(r'\d+',full_desc)#正则提取数量
    #微信会话列表内ListItem标准格式:备注\s(已置顶)\s(\d+)条未读\s最后一条消息内容\s时间
    new_message_pattern=re.compile(r'\n\[(\d+)条\]')#只给数量分组.group(1)获取
    if not new_message_num:
        print(f'没有新消息')
        return {}
    if new_message_num:
        new_message_num=int(new_message_num.group(0))
        session_list=main_window.child_window(**Main_window.ConversationList)
        session_list.type_keys('{END}')
        time.sleep(0.2)
        last_item=session_list.children(control_type='ListItem')[-1].window_text()
        session_list.type_keys('{HOME}')
        time.sleep(0.2)
        count = 0
        while count<new_message_num:#当最终的新消息总数之和大于等于实际新消息总数时退出循环
            #遍历获取带有新消息的ListItem
            listItems=session_list.children(control_type='ListItem')
            time.sleep(delay)
            senders,nums,newMessageTips=traverse_messsage_list(listItems)
            
            ##提取姓名和数量
            count += sum(nums)
            newMessageNums.extend(nums)
            newMessageSenders.extend(senders)
            newMessageTipList.extend(newMessageTips)
            newMessages_dict=dict(zip(newMessageSenders,newMessageTipList))
            session_list.type_keys('{PGDN}')
            if listItems[-1].window_text()==last_item:
                break
        session_list.type_keys('{HOME}')
        not_={'QQ邮箱提醒','微信支付','微信游戏'}
        newMessages_dict=[{sender:tip} for sender,tip in newMessages_dict.items() if sender not in not_]
    if close_weixin:
        main_window.close()
    return newMessages_dict