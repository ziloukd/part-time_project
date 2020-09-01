"""
主程序启动窗户
"""
import os, sys

from core import src


# 1.添加环境变量
BASE_PATH = sys.path.append(
    os.path.dirname('__file__')
)


if __name__ == '__main__':
    src.run()