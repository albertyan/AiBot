import asyncio
import uvicorn
import webview
from utils.log_util import logger
import backend_init 

import random
from io import StringIO
from threading import Thread
from contextlib import redirect_stdout

# import baseUtil
from app import app as fastApp
from environment import env, EnvMode
import mimetypes

mimetypes.add_type("application/javascript", ".js")

envMode = env

def find_port():
    global port
    while True:
        try:
            # port=baseUtil.find_port(port)
            logger.info(f" Uviconserver  port:{port}")
            break
        except Exception as e:
            logger.error(f"Exception Uviconserver error repeat port:{port}")
            port = random.randint(18000, 20000)

def uviconserver():
    global port
    uvicorn.run(app=fastApp, host="localhost", port=port)

def uviconserverThread():
    uvth=Thread(target=uviconserver)
    uvth.daemon = True
    uvth.start()


def fastServer(envmode):
    """
    根据模式启动
    @param envMode:  dev，开发环境，prod，打包环境
    @return:
    """
    stream = StringIO(envmode)
    with redirect_stdout(stream):
        if envmode=="dev":
            # "http://localhost:3000" 前端node启动时的端口号，在vite.config.js 中配置
            window = webview.create_window('AiBot', "http://localhost:3000", width=1024, height=800)
        else:
            window = webview.create_window('AiBot', "http://localhost:"+str(port), width=1024, height=800)
        webview.start(debug=(envmode == "dev"))

#默认端口号，如果重复则随机选取一个
port =3000

if __name__ == '__main__':
    asyncio.run(backend_init.main())
    envMode.set_mode(EnvMode.DEV)
    # find_port()
    uviconserverThread()
    fastServer(envMode.envMode)

    
