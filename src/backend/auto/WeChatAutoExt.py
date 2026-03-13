import re
from auto.WeChatToolsExt import NavigatorExt, ToolsExt
from auto.pyweixin.utils import Regex_Patterns
from auto.UielementsExt import CustomsExt,GroupsExt,SideBarExt,ListItemsExt, ListsExt
from .pyweixin.WeChatAuto import AutoReply, Call, Collections, Contacts, FriendSettings, Files, Settings, Moments, Messages, Monitor
from auto.WeChatBot import WeChatBot
CustomsExt=CustomsExt()
GroupsExt=GroupsExt()
SideBarExt=SideBarExt()

class AutoReplyExt(AutoReply):
    '''
    自动回复扩展类
    '''
    def __init__(self):
        super().__init__()

class CallExt(Call):
    '''
    拨打电话扩展类
    '''
    def __init__(self):
        super().__init__()

class CollectionsExt(Collections):
    '''
    收藏扩展类
    '''
    def __init__(self):
        super().__init__()

class ContactsExt(Contacts):
    '''
    联系人扩展类
    '''
    def __init__(self):
        super().__init__()

    def scan_new_friends(self)->int:
        '''
        该函数用来扫描新的朋友
        Returns:
            new_friends:新的朋友信息
        '''
        main_window = WeChatBot.find_window()
        contacts_button=main_window.child_window(**SideBarExt.Contacts)
        #左上角微信按钮的红色消息提示(\d+条新消息)在FullDescription属性中,
        #只能通过id来获取,id是30159，之前是30007,可能是qt组件映射关系不一样
        full_desc=contacts_button.element_info.element.GetCurrentPropertyValue(30159)
        new_friend_num=re.search(r'\d+',full_desc)#正则提取数量
        print(new_friend_num.group(0))
        if not new_friend_num:
            print(f'没有新的朋友')
            return 0
        if new_friend_num:
            new_friend_num=int(new_friend_num.group(0))
        return new_friend_num
    
    @staticmethod
    def get_new_friends(is_maximize:bool=None,close_weixin:bool=None)->list[tuple[str]]:
        '''
        该函数用来获取新的朋友
        Args:

            is_maximize:微信界面是否全屏，默认不全屏
            close_weixin:任务结束后是否关闭微信，默认关闭
        Returns:
            new_friends:新的朋友信息
        '''
        def remove_duplicates(list):
            seen=set()
            result=[]
            for item in list:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            return result
    
        def get_specific_info(texts):
            nums=[num_pattern.search(text).group(1) for text in texts]
            names=[num_pattern.sub('',text) for text in texts]
            return names,nums

        if is_maximize is None:
            is_maximize=GlobalConfig.is_maximize
        if close_weixin is None:
            close_weixin=GlobalConfig.close_weixin




        #通讯录列表
        contact_list,main_window=Navigator.open_contacts(is_maximize=is_maximize)
        #右侧的自定义面板
        contact_custom=main_window.child_window(**CustomsExt.AddNewFriendCustom)

        texts=[]
        num_pattern=Regex_Patterns.GroupMember_Num_pattern
        contacts_manage=Navigator.open_contacts_manage(is_maximize=is_maximize,close_weixin=close_weixin)
        contacts_manage_list=contacts_manage.child_window(**Lists.ContactsManageList)
        recent_group=contacts_manage.child_window(**ListItems.RecentGroupListItem)
        Tools.collapse_contact_manage(contacts_manage)
        if not recent_group.exists(timeout=0.1):
            print(f'无最近群聊,无法获取!')
            contacts_manage.close()
            return []
        else:
            recent_group.click_input()
            contacts_manage_list.type_keys('{END}',pause=1)
            last=contacts_manage_list.children(control_type='ListItem',
            class_name="mmui::ContactsManagerControlSessionCell")[-1].window_text()
            contacts_manage_list.type_keys('{HOME}')
            listitems=contacts_manage_list.children(control_type='ListItem',class_name="mmui::ContactsManagerControlSessionCell")
            texts.extend([listitem.window_text() for listitem in listitems])
            while texts[-1]!=last:
                contacts_manage_list.type_keys('{PGDN}')
                listitems=contacts_manage_list.children(control_type='ListItem',class_name="mmui::ContactsManagerControlSessionCell")
                texts.extend([listitem.window_text() for listitem in listitems])
            texts=remove_duplicates(texts)#去重,Texts内是群聊+(人数)构成的文本,如果群聊名称与人数都相同那就没法筛选了
            group_names,member_nums=get_specific_info(texts)#正则提取与替换便是群名与人数
            recent_groups=list(zip(group_names,member_nums))#不使用dict(zip)是考虑到可能有相同群聊的,dict key不能有重复
            contacts_manage.close()
            return recent_groups

class FriendSettingsExt(FriendSettings):
    '''
    好友设置扩展类
    '''
    def __init__(self):
        super().__init__()

class FilesExt(Files):
    '''
    文件扩展类
    '''
    def __init__(self):
        super().__init__()

class SettingsExt(Settings):
    '''
    设置扩展类
    '''
    def __init__(self):
        super().__init__()

class MomentsExt(Moments):
    '''
    朋友圈扩展类
    '''
    def __init__(self):
        super().__init__()
        
class MessagesExt(Messages):
    '''
    消息扩展类
    '''
    def __init__(self):
        super().__init__()
        
class MonitorExt(Monitor):
    '''
    监控扩展类
    '''
    def __init__(self):
        super().__init__()
        

