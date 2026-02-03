import time
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

from utils.response_util import ResponseUtil

PopUpProfileWindow = PopUpProfileWindow()

Timings.slow()

home_router = APIRouter()

@home_router.get("/init")
def init() -> Any:
    return ResponseUtil.success(msg="Welcome to the AI Bot API!")

@home_router.get("/dashboard")
async def get_dashboard_data(db: AsyncSession = Depends(get_db)) -> Any : 
    # Get user info (Assuming single user or taking the first one for now)
    main_window= NavigatorExt.open_weixin()
    ToolsExt.cancel_pin(main_window)
    time.sleep(0.5)
    # 检查微信是否运行
    is_running = ToolsExt.is_weixin_running()
    logger.info(f"微信是否运行中: {is_running}")
    if not is_running:
        logger.error("微信未运行，请先启动微信")
        return ResponseUtil.error("微信未运行，请先启动微信")
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
