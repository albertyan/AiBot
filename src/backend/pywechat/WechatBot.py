import os 
import re
import time
import json
import pyautogui
from warnings import warn
from .Warnings import LongTextWarning,ChatHistoryNotEnough
from .WechatTools import Tools,mouse,Desktop
from .WinSettings import Systemsettings
from .Errors import NoWechat_number_or_Phone_numberError
from .Errors import PrivacyNotCorrectError
from .Errors import EmptyFileError
from .Errors import EmptyFolderError
from .Errors import NotFileError
from .Errors import NotFolderError
from .Errors import CantCreateGroupError
from .Errors import NotFriendError
from .Errors import NoPermissionError
from .Errors import SameNameError
from .Errors import AlreadyCloseError
from .Errors import AlreadyInContactsError
from .Errors import EmptyNoteError
from .Errors import NoChatHistoryError
from .Errors import CantSendEmptyMessageError
from .Errors import WrongParameterError
from .Errors import TimeNotCorrectError
from .Errors import TickleError
from .Errors import ElementNotFoundError
from .Uielements import (Main_window,SideBar,Independent_window,Buttons,SpecialMessages,
Edits,Texts,TabItems,Lists,Panes,Windows,CheckBoxes,MenuItems,Menus,ListItems)
from .WechatTools import match_duration

from pywinauto.controls.uia_controls import ListViewWrapper

from coze.chat_no_stream import *
from cozepy import MessageType

#######################################################################################
language=Tools.language_detector()#有些功能需要判断语言版本
Main_window=Main_window()#主界面UI
SideBar=SideBar()#侧边栏UI
Independent_window=Independent_window()#独立主界面UI
Buttons=Buttons()#所有Button类型UI
Edits=Edits()#所有Edit类型UI
Texts=Texts()#所有Text类型UI
TabItems=TabItems()#所有TabIem类型UI
Lists=Lists()#所有列表类型UI
Panes=Panes()#所有Pane类型UI
Windows=Windows()#所有Window类型UI
CheckBoxes=CheckBoxes()#所有CheckBox类型UI
MenuItems=MenuItems()#所有MenuItem类型UI
Menus=Menus()#所有Menu类型UI
ListItems=ListItems()#所有ListItem类型UI
SpecialMessages=SpecialMessages()#特殊消息
pyautogui.FAILSAFE=False#防止鼠标在屏幕边缘处造成的误触


@staticmethod
def get_myself_name():
    '''
    该方法用来获取当前登录用户的名称\n
    返回值为str类型,即当前登录用户的名称
    '''
    main_window=Tools.open_wechat(is_maximize=False)
    myname=main_window.child_window(**Buttons.MySelfButton).window_text()
    weixinno=main_window.window(**Windows.ContactProfileWindow).Static3.window_text()
    return myname, weixinno



@staticmethod
def init_group_alias(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该方法用来获取通讯录中所有群聊的信息(名称,昵称,成员数量)\n
    结果以json格式返回\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    def get_info(group_chat_list):
        names=[chat.children()[0].children()[0].children(control_type="Button")[0].texts()[0] for chat in group_chat_list]
        numbers=[chat.children()[0].children()[0].children()[1].children()[0].children()[1].texts()[0] for chat in group_chat_list]
        numbers=[number.replace('(','').replace(')','') for number in numbers]
        return names,numbers
    
    def get_group_alias(names,search_pages:int=0):
        myaliasarr = []
        #####################################################################################
        for name in names:
            #打开群聊右侧的设置界面,看一看我的群昵称是什么,这样是为了判断我是否被@
            Tools.find_friend_in_MessageList(friend=name)
            voice_call_button=main_window.child_window(**Buttons.VoiceCallButton)#语音聊天按钮
            video_call_button=main_window.child_window(**Buttons.VideoCallButton)#视频聊天按钮
            if voice_call_button.exists() and not video_call_button.exists():#只有语音和聊天按钮没有视频聊天按钮是群聊
                ChatMessage=main_window.child_window(**Buttons.ChatMessageButton)
                ChatMessage.click_input()
                group_settings_window=main_window.child_window(**Main_window.GroupSettingsWindow)
                group_settings_window.child_window(**Texts.GroupNameText).click_input()
                group_settings_window.child_window(**Buttons.MyAliasInGroupButton).click_input() 
                change_my_alias_edit=group_settings_window.child_window(**Edits.EditWnd)
                change_my_alias_edit.click_input()
                myalias=change_my_alias_edit.window_text()#我的群昵称
                myaliasarr.append(myalias)
            else:
                myaliasarr.append('#nothing#')
        return myaliasarr
    
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    contacts_settings_window=Tools.open_contacts_manage(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)[0]
    recent_group_chat=contacts_settings_window.child_window(**Buttons.RectentGroupButton)
    try:
        group_chat_list_item=contacts_settings_window.child_window(control_type="List",found_index=0,title="").children(control_type="ListItem",title="")      
        first_group=group_chat_list_item[0].children()[0].children()[0].children(control_type="Button")[0]
        first_group.click_input()
    except IndexError:
        recent_group_chat.set_focus()
        recent_group_chat.click_input()
        group_chat_list_item=contacts_settings_window.child_window(control_type="List",found_index=0,title="").children(control_type="ListItem",title="")      
        first_group=group_chat_list_item[0].children()[0].children()[0].children(control_type="Button")[0]
        first_group.click_input()
    
    pyautogui.press('End')
    group_chat_list_item=contacts_settings_window.child_window(control_type="List",found_index=0,title="").children(control_type="ListItem",title="")
    last_group_name=get_info(group_chat_list_item)[0][-1]
    pyautogui.press('Home')
    temp=[last_group_name,'nothing']#记录最后一个群的群聊名称，和get_friends_info一样的思路
    groups_members=[]
    groups_names=[]
    record1=[]
    record2=[]
    while temp[-1]!=temp[0]:#比较temp中记录的群聊名称有没有和temp首个元素相同，若相同说明已经到达底部，结束循环
        group_chat_list_item=contacts_settings_window.child_window(control_type="List",found_index=0,title="").children(control_type="ListItem",title="")      
        names,numbers=get_info(group_chat_list_item)
        temp.append(names[-1])
        record1.extend(names)
        record2.extend(numbers)
        pyautogui.press("pagedown",_pause=False)
    contacts_settings_window.close()
    temp.clear()
    
    for index, value in enumerate(record1):
        if value not in groups_names:
            groups_names.append(value)
            groups_members.append(record2[index])
    myaliasarr = get_group_alias(groups_names, search_pages=0)
    record=zip(groups_names, myaliasarr, groups_members)

    groups_info=[{"群聊名称":group[0],"群昵称":group[1],"群聊人数":group[2]} for group in record if group[1] != '#nothing#'] #过滤掉没有群昵称的群聊
    groups_info_json=json.dumps(groups_info,indent=4,ensure_ascii=False)
    return groups_info_json

@staticmethod
def AI_auto_reply_to_friend1(message:dict,AI_engine=None,save_chat_history:bool=False,capture_screen:bool=False,folder_path:str=None,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来接入AI大模型自动回复好友消息\n
    Args:
        friend:\t好友或群聊备注\n
        duration:\t自动回复持续时长,格式:'s','min','h'单位:s/秒,min/分,h/小时\n
        Ai_engine:\t调用的AI大模型API函数,去各个大模型官网找就可以\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏法搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    friend = message['名称'] 

    if not AI_engine:
        AI_engine = ai_engine

    if save_chat_history and capture_screen and folder_path:#需要保存自动回复后的聊天记录截图时，可以传入一个自定义文件夹路径，不然保存在运行该函数的代码所在文件夹下
        #当给定的文件夹路径下的内容不是一个文件夹时
        if not Systemsettings.is_dirctory(folder_path):#
            raise NotFolderError(r'给定路径不是文件夹!无法保存聊天记录截图,请重新选择文件夹！')

    #打开好友的对话框,返回值为编辑消息框和主界面
    chat,main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    #需要判断一下是不是公众号
    voice_call_button=main_window.child_window(**Buttons.VoiceCallButton)
    video_call_button=main_window.child_window(**Buttons.VideoCallButton)
    if not voice_call_button.exists():
        #公众号没有语音聊天按钮
        main_window.close()
        raise NotFriendError(f'非正常好友,无法自动回复!')
    # if video_call_button.exists() and voice_call_button.exists():
    #     type='好友'
    if not video_call_button.exists() and voice_call_button.exists():
        # type='群聊'
        myname=main_window.child_window(control_type='Button',found_index=0).window_text()#自己的名字
    #####################################################################################
    chatList=main_window.child_window(**Main_window.FriendChatList)#聊天界面内存储所有信息的容器 
    Systemsettings.open_listening_mode(volume=False)#开启监听模式,此时电脑只要不断电不会息屏 


    newMessage = message['消息'][0]
    who = message['名称']
    
    type = message['类型']

    print(f'新消息: {newMessage}, 发送者: {who}, 类型: {type}')

    #消息列表内的最后一条消息(listitem)不等于刚打开聊天界面时的最后一条消息(listitem)
    #并且最后一条消息的发送者是好友时自动回复
    #这里我们判断的是两条消息(listitem)是否相等,不是文本是否相等,要是文本相等的话,对方一直重复发送
    #刚打开聊天界面时的最后一条消息的话那就一直不回复了
    if type=='好友':
        chat.click_input()
        Systemsettings.copy_text_to_windowsclipboard(AI_engine(newMessage))#复制回复内容到剪贴板
        pyautogui.hotkey('ctrl','v',_pause=False)
        pyautogui.hotkey('alt','s',_pause=False)

    if type=='群聊':
        chat.click_input()
        Systemsettings.copy_text_to_windowsclipboard(AI_engine(newMessage))#复制回复内容到剪贴板
        pyautogui.hotkey('ctrl','v',_pause=False)
        pyautogui.hotkey('alt','s',_pause=False)

    Systemsettings.close_listening_mode()
    if close_wechat:
        main_window.close()


@staticmethod
def ai_engine(msg:str):
    '''
    该函数是一个AI大模型API函数的示例,你可以将其替换为你自己的AI大模型API函数\n
    Args:
        message:\t需要传入的消息内容
    Returns:
        str:返回回复内容
    '''
    print(f"送入到大模型的消息: {msg}")
    # Init the Coze client through the access_token.
    coze = Coze(auth=TokenAuth(token=get_coze_api_token()), base_url=get_coze_api_base())
    # Create a bot instance in Coze, copy the last number from the web link as the bot's ID.
    bot_id = os.getenv("COZE_BOT_ID") or "7502317234447728678"
    # The user id identifies the identity of a user. Developers can use a custom business ID
    # or a random string.
    user_id = "123"

    
    # To simplify the call, the SDK provides a wrapped function to complete non-streaming chat,
    # polling, and obtaining the messages of the chat. Developers can use create_and_poll to
    # simplify the process.
    chat_poll = coze.chat.create_and_poll(
        bot_id=bot_id,
        user_id=user_id,
        additional_messages=[
            Message.build_user_question_text(msg)
        ],
    )

    # while chat_poll.chat.status == ChatStatus.COMPLETED:
    # When the chat status becomes completed, all messages under this chat can be retrieved through the list messages interface.


    for message in chat_poll.messages:
        if (message.type == MessageType.ANSWER):
            # 这里可以处理AI大模型的回复内容
            # 例如，返回回复内容
            if message.content:
                print(f"\nAI回复: {message.content}")
            else:
                print("\nAI回复: 无内容")
            return message.content

    # if chat_poll.chat.status == ChatStatus.COMPLETED:
    #     print()
    #     print("token usage:", chat_poll.chat.usage.token_count)

    # 这里可以调用你的AI大模型API进行处理
    # 例如，使用OpenAI的GPT-3.5 API
    return f""  # 示例返回内容