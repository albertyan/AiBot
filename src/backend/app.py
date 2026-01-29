''' -*- coding: utf-8 -*-
# @Author  : Ficus
# @Time    : 2024/11/2 09:36
# @File    : fastServer.py
'''
import os
import logging
from typing import Dict, Any

from pydantic import BaseModel
from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
import mimetypes

# 修复 Windows 下 .js 文件 MIME 类型可能为 text/plain 导致前端无法加载的问题
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")

from router import router_manager
from api import home_router, setting_router
# import baseUtil

# 前端文件目录
BASE_DIR = os.path.abspath(os.getcwd())
dist_dir = os.path.join(BASE_DIR, "dist", "gui")
# dist_dir = os.path.join(baseUtil.get_exe_path(), "gui")
static_dir = os.path.join(dist_dir, "assets")

app = FastAPI(docs_url=None)

# 注册路由
app.include_router(router_manager.router)
app.include_router(setting_router, prefix="/api", tags=["config"])
app.include_router(home_router, prefix="/api/home", tags=["home"])
app.mount("/assets", StaticFiles(directory=static_dir), name="assets")


class BaseMap(BaseModel):
    data: Dict[str, Any]
