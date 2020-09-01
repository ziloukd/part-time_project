# -*- coding: utf-8 -*-
import os


income_dict = {
    'a1': '生活费',
    'a2': '红包奖金',
    'a3': '兼职',
}

expenditure_dict = {
    'b1': '学习用品',
    'b2': '生活用品',
    'b3': '餐饮美食',
}

BASE_PATH = os.path.dirname(
    os.path.dirname('__file__')
)

DB_PATH = os.path.join(
    BASE_PATH, 'db'
)
