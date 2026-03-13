from .pyweixin.Uielements import (Login_window,Main_window, MenuItems,SideBar,Independent_window,ListItems,
Buttons,Texts,Menus,TabItems,Lists,Edits,Windows,Panes,Customs,Groups)

class Login_windowExt(Login_window):
    def __init__(self):
        super().__init__()

class Main_windowExt(Main_window):
    def __init__(self):
        super().__init__()

class SideBarExt(SideBar):
    def __init__(self):
        super().__init__()

class Independent_windowExt(Independent_window):
    def __init__(self):
        super().__init__()

class ListItemsExt(ListItems):
    def __init__(self):
        super().__init__()
        
class ButtonsExt(Buttons):
    def __init__(self):
        super().__init__()

class TextsExt(Texts):
    def __init__(self):
        super().__init__()

class MenusExt(Menus):
    def __init__(self):
        super().__init__()

class TabItemsExt(TabItems):
    def __init__(self):
        super().__init__()

class ListsExt(Lists):
    def __init__(self):
        super().__init__()

class EditsExt(Edits):
    def __init__(self):
        super().__init__()

class WindowsExt(Windows):
    def __init__(self):
        super().__init__()
        self.NewFriendVerifyFriendWindow={'control_type':'Window','title':'通过朋友验证','class_name':'mmui::VerifyFriendWindow'}#添加新朋友时的申请添加朋友界面
        
class PanesExt(Panes):
    def __init__(self):
        super().__init__()
        
class MenuItemsExt(MenuItems):
    def __init__(self):
        super().__init__()

class CustomsExt(Customs):
    def __init__(self):
        super().__init__()
        self.AddNewFriendCustom={'control_type':'Custom','auto_id':'main_window_sub_splitter_view','class_name':'mmui::XSplitterView'}#微信切换到通讯录界面后的右侧好友信息面板的上一级自定义

class PopUpProfileWindow():
    def __init__(self):
        super().__init__()
        self.ContactProfileTextView = {'control_type':'Text','class_name':'mmui::ContactProfileTextView'} # 个人中心面板文本
        self.ContactProfileNicknameTextView = {'control_type':'Text','class_name':'mmui::XTextView'} # 个人中心面板文本

class GroupsExt(Groups):
    def __init__(self):
        super().__init__()
        self.AddNewFriendGroup={'title':'','control_type':'Group','class_name':'mmui::ContactProfileView'}#添加好友面板
