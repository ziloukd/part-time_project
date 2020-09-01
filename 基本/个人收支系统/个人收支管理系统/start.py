# -*- coding: utf-8 -*-
'''
系统界面
'''
import os, sys


from core.src import run


#1.添加环境变量
BASE_PATH = sys.path.append(
    os.path.dirname('__file__')
)


if __name__ == '__main__':
    run()