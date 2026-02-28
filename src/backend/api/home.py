import time
import os
import subprocess
import asyncio
import winreg
from typing import Any
from loguru import logger
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pywinauto.timings import Timings
from pywinauto import mouse

from db.get_db import get_db
from db.models import Friends, Groups, WechatAccounts
from auto.WeChatToolsExt import ToolsExt,NavigatorExt
from auto.UielementsExt import PopUpProfileWindow
from environment import CurrentUser, CurrentUserDep, state

from utils.config_file import check_base_dir, check_personal_dir
from utils.response_util import ResponseUtil

PopUpProfileWindow = PopUpProfileWindow()

Timings.slow()

home_router = APIRouter()

@home_router.get("/init")
def init() -> Any:
    return ResponseUtil.success(msg="Welcome to the AI Bot API!")

@home_router.get("/dashboard")
async def get_dashboard_data(db: AsyncSession = Depends(get_db)) -> Any : 
    # 检查微信是否运行
    is_running = ToolsExt.is_weixin_running()
    logger.info(f"微信是否运行中: {is_running}")
    if not is_running:
        logger.error("微信未运行，请先启动微信")
        return ResponseUtil.error("微信未运行，请先启动微信")
        # Get user info (Assuming single user or taking the first one for now)
    try:
        main_window= NavigatorExt.open_weixin()
        ToolsExt.cancel_pin(main_window)
    except Exception as e:
        logger.error(f"打开微信失败: {e}")
        return ResponseUtil.error(f"打开微信失败: {e}")
    
    time.sleep(0.5)
    # 等待窗口出现
    if not main_window.exists(timeout=0.1):
        logger.error("未找到微信主窗口，请确保已登录并打开主界面")
        return ResponseUtil.error("未找到微信主窗口，请确保已登录并打开主界面")
    
    # 恢复窗口状态（如果最小化）
    try:
        if main_window.get_show_state() == 2: # 2 代表最小化
            main_window.restore()
        main_window.set_focus()
    except Exception as e:
        logger.error(f"窗口操作异常: {e}")
        return ResponseUtil.error(f"窗口操作异常: {e}")
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
        return ResponseUtil.error("个人信息窗口未打开(超时)") 
    # 使用 child_window 配合 found_index 快速获取，避免遍历整个树
    time.sleep(0.5)
    try:
        # mmui::XTextView
        nickname = my.child_window(found_index=0, **PopUpProfileWindow.ContactProfileNicknameTextView).window_text()
        # 尝试获取第一个匹配的控件
        wxNumber = my.child_window(found_index=0, **PopUpProfileWindow.ContactProfileTextView).window_text()
    except Exception as e:
        logger.error(f"获取个人微信号时出错: {e}")
        return ResponseUtil.error(f"获取个人微信号时出错: {e}")
    finally:
        main_window.set_focus()

    logger.info(f"当前个人信息: {wxNumber}, 昵称: {nickname}")
    result = await db.execute(select(WechatAccounts).where(WechatAccounts.account_id == wxNumber))
    my = result.scalar_one_or_none()
    if not my:
        db.add(WechatAccounts(nickname=nickname, account_id=wxNumber))
        await db.commit()
        # 将当前用户写入后端全局状态，原因是后续接口可能需要无数据库查询读取“当前账号”
    else:
        # 更新最后登录时间,用update_time记录
        my.update_time = func.now()
        my.nickname = nickname
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
    return ResponseUtil.success(
            msg=(f"当前微信号: {wxNumber}, 状态: {'在线' if is_running else '离线'}"),
            data={
                "wxNumber": wxNumber,
                "nickname": nickname,
                "friendCount": friend_count,
                "groupCount": group_count,
                "status": "在线" if is_running else "离线"}
            )

@home_router.get("/friendCount")
async def get_friendCount(current_user: CurrentUserDep, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(func.count(Friends.id)).where(Friends.account_id == current_user.wxNumber))
    friend_count = result.scalar()
    return ResponseUtil.success(
        msg="获取好友数量成功",
        data=friend_count
    )

@home_router.get("/groupCount")
async def get_groupCount(current_user: CurrentUserDep, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(func.count(Groups.id)).where(Groups.account_id == current_user.wxNumber))
    group_count = result.scalar()
    return ResponseUtil.success(    
        msg="获取群数量成功",
        data=group_count
    )

@home_router.post("/auto_configure_env")
async def auto_configure_env() -> Any:
    """
    自动配置环境：
    1. 退出微信
    2. 设置windows当前用户环境变量QT_ACCESSIBILITY=1
    3. 启动讲述人(触发Accessibility)
    4. 重启微信
    """
    logger.info("Starting auto configuration for environment...")
    
    # 1. Kill WeChat
    try:
        # Use os.system which is more direct for command execution on Windows
        # Redirect output to nul to suppress noise, but log the action
        logger.info("Attempting to kill WeChat process...")
        result = os.system("taskkill /F /IM Weixin.exe >nul 2>&1")
        if result == 0:
            logger.info("Killed WeChat process successfully")
        else:
            # If WeChat wasn't running, taskkill returns a non-zero exit code (usually 128)
            # which is fine, but we log it just in case
            logger.info(f"Taskkill returned code {result}, WeChat might not be running")
    except Exception as e:
        logger.warning(f"Failed to kill WeChat: {e}")

    # 2. Set current user environment variable QT_ACCESSIBILITY=1
    try:
        # Check if already set
        if os.environ.get("QT_ACCESSIBILITY") != "1":
            # Set for current process and children
            os.environ["QT_ACCESSIBILITY"] = "1"
            # Set persistently for user (System Environment Variable)
            subprocess.run(["setx", "QT_ACCESSIBILITY", "1"], capture_output=True)
            logger.info("Set QT_ACCESSIBILITY=1 in environment variables")
        else:
            logger.info("QT_ACCESSIBILITY is already set to 1, skipping configuration.")
    except Exception as e:
        logger.warning(f"Failed to set environment variable: {e}")

    # 3. Run Narrator for 10s
    try:
        logger.info("Starting Narrator...")
        # Using Narrator.exe might require full path or just command
        # On Windows, Narrator.exe is usually in System32
        os.startfile("Narrator.exe")
        await asyncio.sleep(10)
        subprocess.run(["taskkill", "/F", "/IM", "Narrator.exe"], capture_output=True)
        logger.info("Stopped Narrator")
    except Exception as e:
        logger.error(f"Error running Narrator: {e}")
        return ResponseUtil.error(msg=f"启动讲述人失败: {e}")

    # 4. Restart WeChat
    wechat_path = None
    try:
        wechat_path = ToolsExt.where_weixin()
    except Exception as e:
        logger.warning(f"Failed to find WeChat path from registry: {e}")

    if wechat_path and os.path.exists(wechat_path):
        try:
            logger.info(f"Starting WeChat from {wechat_path}")
            subprocess.Popen([wechat_path])
            return ResponseUtil.success(msg="环境配置完成，微信已重启")
        except Exception as e:
            logger.error(f"Failed to start WeChat: {e}")
            return ResponseUtil.error(msg=f"重启微信失败: {e}")
    else:
        return ResponseUtil.success(msg="环境配置完成，请手动重启微信")
