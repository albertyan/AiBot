from pyweixin.Uielements import (Login_window,Main_window,SideBar,Independent_window,ListItems,
Buttons,Texts,Menus,TabItems,Lists,Edits,Windows,Panes)

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
        
class PanesExt(Panes):
    def __init__(self):
        super().__init__()
        

class PopUpProfileWindow():
    def __init__(self):
        super().__init__()
        self.ContactProfileTextView = {'control_type':'Text','class_name':'mmui::ContactProfileTextView'} # 个人中心面板文本
        self.ContactProfileNicknameTextView = {'control_type':'Text','class_name':'mmui::XTextView'} # 个人中心面板文本