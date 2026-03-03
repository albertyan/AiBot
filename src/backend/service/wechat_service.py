from typing import List, Dict, Any
import re
import time
import os
import asyncio
import subprocess
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pywinauto import mouse
from pywinauto.timings import Timings

from auto.WeChatBot import scan_for_new_messages
from auto.WeChatToolsExt import ToolsExt, NavigatorExt
from auto.UielementsExt import PopUpProfileWindow
from api.schemas import WeChatSession
from db.models import Friends, Groups, WechatAccounts
from environment import CurrentUser, CurrentUserDep, state
from utils.config_file import check_base_dir, check_personal_dir
from utils.perf_util import instrument_class

PopUpProfileWindow = PopUpProfileWindow()

class WeChatService:
    Timings.slow()

    def __init__(self):
        pass

    def get_new_messages(self, wx_number: str) -> List[WeChatSession]:
        """
        扫描微信新消息并解析
        """
        newMessages_list = scan_for_new_messages()
        # newMessages_list is [{'sender': 'raw_string'}, ...]
        
        sessions = []
        for item in newMessages_list:
            # item is a dict with one key
            for sender, raw_content in item.items():
                # Parsing logic
                parts = [p.strip() for p in raw_content.split('\n') if p.strip()]
                
                # Basic parsing logic
                count = 0
                last_message = ""
                last_time = ""
                is_top = "已置顶" in raw_content
                
                # Extract count: [9条]
                count_match = re.search(r'\[(\d+)条\]', raw_content)
                if count_match:
                    count = int(count_match.group(1))
                
                # Extract time: usually last line
                if parts:
                    last_time = parts[-1]
                    
                # Extract message
                msg_content = raw_content
                # Remove sender (at start)
                if msg_content.startswith(sender):
                    msg_content = msg_content[len(sender):]
                
                # Remove status
                msg_content = msg_content.replace("已置顶", "")
                
                # Remove count
                if count_match:
                    msg_content = msg_content.replace(count_match.group(0), "")
                    
                # Remove time (at end)
                msg_content = msg_content.strip()
                if msg_content.endswith(last_time):
                    msg_content = msg_content[:-len(last_time)]
                    
                last_message = msg_content.strip()
                
                sessions.append(WeChatSession(
                    id=sender, # use sender name as ID
                    name=sender,
                    count=count,
                    last_message=last_message,
                    last_time=last_time,
                    is_top=is_top,
                    raw_content=raw_content,
                    source=wx_number
                ))
        return sessions

    async def get_dashboard_data(self, db: AsyncSession) -> Dict[str, Any]:
        """
        获取仪表盘数据：微信状态、个人信息、好友数量、群数量
        """
        # 检查微信是否运行
        is_running = ToolsExt.is_weixin_running()
        logger.info(f"微信是否运行中: {is_running}")
        if not is_running:
            logger.error("微信未运行，请先启动微信")
            raise Exception("微信未运行，请先启动微信")
        
        try:
            main_window= NavigatorExt.open_weixin()
            ToolsExt.cancel_pin(main_window)
        except Exception as e:
            logger.error(f"打开微信失败: {e}")
            raise Exception(f"打开微信失败: {e}")
        
        time.sleep(0.5)
        # 等待窗口出现
        if not main_window.exists(timeout=0.1):
            logger.error("未找到微信主窗口，请确保已登录并打开主界面")
            raise Exception("未找到微信主窗口，请确保已登录并打开主界面")
        
        # 恢复窗口状态（如果最小化）
        try:
            if main_window.get_show_state() == 2: # 2 代表最小化
                main_window.restore()
            main_window.set_focus()
        except Exception as e:
            logger.error(f"窗口操作异常: {e}")
            raise Exception(f"窗口操作异常: {e}")
            
        # 获取窗口对象和坐标
        main = main_window.wrapper_object()
        rect = main.rectangle()
        logger.info(f"窗口坐标范围: {rect}")
        mouse.click(coords=(rect.left + 33, rect.top + 55)) 

        time.sleep(0.5)
        my=NavigatorExt.find_my_info_window()
        try:
            my.wait('exists', timeout=2) # 等待窗口出现，避免 ElementNotFoundError
            logger.info("个人信息窗口已打开")
        except Exception:
            logger.error("个人信息窗口未打开(超时)")
            raise Exception("个人信息窗口未打开(超时)") 
            
        # 使用 child_window 配合 found_index 快速获取，避免遍历整个树
        time.sleep(0.5)
        try:
            # mmui::XTextView
            nickname = my.child_window(found_index=0, **PopUpProfileWindow.ContactProfileNicknameTextView).window_text()
            # 尝试获取第一个匹配的控件
            wxNumber = my.child_window(found_index=0, **PopUpProfileWindow.ContactProfileTextView).window_text()
        except Exception as e:
            logger.error(f"获取个人微信号时出错: {e}")
            raise Exception(f"获取个人微信号时出错: {e}")
        finally:
            main_window.set_focus()

        logger.info(f"当前个人信息: {wxNumber}, 昵称: {nickname}")
        result = await db.execute(select(WechatAccounts).where(WechatAccounts.account_id == wxNumber))
        my_account = result.scalar_one_or_none()
        if not my_account:
            db.add(WechatAccounts(nickname=nickname, account_id=wxNumber))
            await db.commit()
        else:
            # 更新最后登录时间,用update_time记录
            my_account.update_time = func.now()
            my_account.nickname = nickname
            await db.commit()
            
        state.set_current_user(CurrentUser(nickname=nickname, number=wxNumber))
        
        # 获取好友数量
        stmt = select(func.count(Friends.id)).where(Friends.account_id == wxNumber)
        result = await db.execute(stmt)
        friend_count = result.scalar()
        
        # 获取群数量
        stmt = select(func.count(Groups.id)).where(Groups.account_id == wxNumber)
        result = await db.execute(stmt)
        group_count = result.scalar()
        
        # 检查用户目录是否存在， 如果不存在则创建
        check_base_dir()
        # 检查个人目录是否存在， 如果不存在则创建
        check_personal_dir(wxNumber)
        
        return {
            "wxNumber": wxNumber,
            "nickname": nickname,
            "friendCount": friend_count,
            "groupCount": group_count,
            "status": "在线" if is_running else "离线",
            "is_running": is_running
        }

    async def auto_configure_env(self):
        """
        自动配置环境
        """
        logger.info("Starting auto configuration for environment...")
        
        # 1. Kill WeChat
        try:
            logger.info("Attempting to kill WeChat process...")
            result = os.system("taskkill /F /IM Weixin.exe >nul 2>&1")
            if result == 0:
                logger.info("Killed WeChat process successfully")
            else:
                logger.info(f"Taskkill returned code {result}, WeChat might not be running")
        except Exception as e:
            logger.warning(f"Failed to kill WeChat: {e}")

        # 2. Set current user environment variable QT_ACCESSIBILITY=1
        try:
            if os.environ.get("QT_ACCESSIBILITY") != "1":
                os.environ["QT_ACCESSIBILITY"] = "1"
                subprocess.run(["setx", "QT_ACCESSIBILITY", "1"], capture_output=True)
                logger.info("Set QT_ACCESSIBILITY=1 in environment variables")
            else:
                logger.info("QT_ACCESSIBILITY is already set to 1, skipping configuration.")
        except Exception as e:
            logger.warning(f"Failed to set environment variable: {e}")

        # 3. Run Narrator for 10s
        try:
            logger.info("Starting Narrator...")
            os.startfile("Narrator.exe")
            await asyncio.sleep(10)
            subprocess.run(["taskkill", "/F", "/IM", "Narrator.exe"], capture_output=True)
            logger.info("Stopped Narrator")
        except Exception as e:
            logger.error(f"Error running Narrator: {e}")
            raise Exception(f"启动讲述人失败: {e}")

        # 4. Restart WeChat
        wechat_path = None
        try:
            wechat_path = ToolsExt.where_weixin()
        except Exception as e:
            # Ignore
            pass
            
        if wechat_path:
             try:
                 logger.info(f"Restarting WeChat from: {wechat_path}")
                 os.startfile(wechat_path)
             except Exception as e:
                 logger.error(f"Failed to start WeChat: {e}")
                 raise Exception(f"启动微信失败: {e}")
        else:
             logger.warning("Could not find WeChat path to restart")
             raise Exception("未找到微信安装路径，无法自动重启")

WeChatService = instrument_class(WeChatService, prefix="service.WeChatService")
wechat_service = WeChatService()
