''' -*- coding: utf-8 -*-
# @Author  : Ficus
# @Time    : 2024/11/5 15:34
# @File    : util.py
'''
import os
import sys
import subprocess
from pathlib import Path
import socketserver
def get_root_path():
    '''
    获取项目根目录
    '''
    if hasattr(sys,'_MEIPASS'):
        return sys._MEIPASS

    return os.path.abspath(os.path.dirname(__file__))

def get_exe_path():
    if getattr(sys, 'frozen', False):
        # 获取可执行文件所在的目录
        BASE_PATH = os.path.dirname(sys.executable)
        # print(f'脚本执行路径：{BASE_PATH}')
        # 将当前工作目录设置为可执行文件所在的目录
        #os.chdir(BASE_PATH)
        return BASE_PATH
    else:
        # 如果程序作为脚本运行，使用脚本目录
        BASE_PATH = os.path.dirname(__file__)
        # print(f'脚本执行路径：{BASE_PATH}')
        #os.chdir(BASE_PATH)
        return BASE_PATH

def find_port(port=None):
    port = 0 if port is None else port
    with socketserver.TCPServer(("localhost",port),None) as server:
        return server.server_address[1]


def build(cmd=""):
    '''
    打包成exe
    '''
    # 激活conda环境 没有则不用

    result=subprocess.run(cmd+ " && pyinstaller AIBOT.spec",shell=True,capture_output=True,text=True)
    print(result)



if __name__ == '__main__':
    root_path=get_root_path()
    print("root_path",root_path)
    print(f'findport:{find_port(8000)}')
    build("conda activate py31016")
