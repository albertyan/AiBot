############################依赖环境###########################

import re
import time
import pyautogui
import win32gui
from pyweixin.Config import GlobalConfig
from pywinauto import mouse,Desktop
from pywinauto.controls.uia_controls import ListViewWrapper,ListItemWrapper,EditWrapper #TypeHint要用到
from pywinauto import WindowSpecification
from pyweixin.Uielements import (Login_window,Main_window,SideBar,Independent_window,ListItems,
Buttons,Texts,Menus,TabItems,Lists,Edits,Windows,Panes)
from pyweixin.WinSettings import SystemSettings 
##########################################################################################

#各种UI实例化
Login_window=Login_window()#登录界面的UI
Main_window=Main_window()#主界面UI
SideBar=SideBar()#侧边栏UI
Independent_window=Independent_window()#独立主界面UI
Buttons=Buttons()#所有Button类型UI
Texts=Texts()#所有Text类型UI
TabItems=TabItems()#所有TabIem类型UI
Lists=Lists()#所有列表类型UI
Menus=Menus()#所有Menu类型UI
Edits=Edits()#所有Edits类型UI
Windows=Windows()#所有Window类型UI
Panes=Panes()#所有Pane类型UI
ListItems=ListItems()#所有ListItem类型UI
desktop=Desktop(backend='uia')#Window桌面
pyautogui.FAILSAFE=False#防止鼠标在屏幕边缘处造成的误触

from pyweixin.WeChatTools import WxWindowManage, Tools, Navigator

class WxWindowManageExt(WxWindowManage) :
    def __init__(self, class_name_re:str):
        super().__init__()
        self.class_name_re=re.compile(class_name_re)

    def find_my_info_window(self)->WindowSpecification:
        '''
        查找我的信息窗口
        '''
        def filterWindow(hwnd, param):
            # self.class_name_re = re.compile(r'Qt\d+QWindowToolSaveBits')
            #EnumDesktopWindows的回调函数
            classname=win32gui.GetClassName(hwnd)
            if self.class_name_re.match(classname):
                self.possible_windows.append(hwnd) 

        win32gui.EnumDesktopWindows(0,filterWindow,None)  
        self.possible_windows=[hwnd for hwnd in self.possible_windows if 'mmui::ProfileUniquePop' in desktop.window(handle=hwnd).class_name()]
        if self.possible_windows:
            self.hwnd=self.possible_windows[0]
        return self.hwnd

class ToolsExt(Tools):
    def __init__(self):
        super().__init__()

    
class NavigatorExt(Navigator):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def find_my_info_window()->WindowSpecification:
        '''
        打开我的信息窗口
        '''
        wx=WxWindowManageExt(r'Qt\d+QWindowToolSaveBits')

        handle=wx.find_my_info_window()
        while not handle:
            handle=wx.find_my_info_window()
            time.sleep(0.1)
        my_info_window=desktop.window(handle=handle)
        return my_info_window