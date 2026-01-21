''' -*- coding: utf-8 -*-
# @Author  : Ficus
# @Time    : 2024/11/4 15:14
# @File    : server.py
'''
import os

from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse
from loguru import logger
from environment import env, EnvMode
import importlib.util

router = APIRouter()

# if env.envMode == EnvMode.DEV:
#     from src import baseUtil
# else:
#     import baseUtil

BASE_DIR = os.path.abspath(os.getcwd())

dist_dir = os.path.join(BASE_DIR, "dist\\gui")

@router.get("/",response_class=HTMLResponse)
def hello():
    indexpath = os.path.join(dist_dir,"index.html")
    print(indexpath)
    with open(indexpath) as f:
        return f.read()
    
@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    print(os.path.join(dist_dir, "favicon.ico"))
    return FileResponse(os.path.join(dist_dir, "favicon.ico"))

# 新增心跳/检查接口
@router.get("/c_hello")
def c_hello(asker: str = None):
    return {"message": "hello", "asker": asker}