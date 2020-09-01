# -*- coding: utf-8 -*-
'''
逻辑接口层
'''
import re
from db import db_handler
from common import setting

def detail_save_interface(detail):
    # 1.检查写入格式是否符合规范
    detail_list = detail.split(',')

    if len(detail_list) < 3:
        return False, '写入失败!请检查写入格式！'

    if detail_list[0] in setting.income_dict or detail_list[0] in setting.expenditure_dict:
        if re.findall('\d{4}-\d{1,2}-\d{1,2}', detail_list[1]):
            if detail_list[2].isdigit():
                #1.1 符合规范，则调用db_handler的数据保存功能
                db_handler.save(
                    detail
                )
                return True, '写入成功！'

    # 1.2 不符合规范，返回False,写入失败
    return False, '写入失败!请检查写入格式！'


def summary_view_interface(date):
    # 1.检查输入的是否为日期（year-month）
    # 1.1 输入不符合规范，返回False, '请检查输入格式是否有误！'
    if not re.findall('\d{4}-\d{1,2}', date):
        return False, '请检查输入格式是否有误！'

    # 1.2 输入符合规范，调用db_handler的select功能查看数据
    data_list = db_handler.select(
        date
    )
    if not data_list:
        return False, f'{date}没有数据！'

    data_dict = {
        '收入':0,
        '支出':0,
    }
    income = 0
    expenditure = 0
    a1 = 0
    a2 = 0
    a3 = 0
    b1 = 0
    b2 = 0
    b3 = 0

    for data in data_list:
        if 'a1' == data[0]:
            a1 = float(data[2])
            data_dict['a1'] = a1
        if 'a2' == data[0]:
            a2 = float(data[2])
            data_dict['a2'] = a2
        if 'a3' == data[0]:
            a3 += float(data[2])
            data_dict['a3'] = a3
        if 'b1' == data[0]:
            b1 += float(data[2])
            data_dict['b1'] = b1
        if 'b2' == data[0]:
            b2 += float(data[2])
            data_dict['b2'] = b2
        if 'b3' == data[0]:
            b3 += float(data[2])
            data_dict['b3'] = b3
        if 'a' in data[0]:
            income += float(data[2])
            data_dict['收入'] = income
        if 'b' in data[0]:
            expenditure += float(data[2])
            data_dict['支出'] = expenditure
    # 数据汇总， 返回True,data_dict
    return True, data_dict



def detail_view_interface(date):
    # 1.检查输入的是否为日期（year-month）
    # 1.1 输入不符合规范，返回False, '请检查输入格式是否有误！'
    if not re.findall('\d{4}-\d{1,2}', date):
        return False, '请检查输入格式是否有误！'

    # 1.2 输入符合规范，调用db_handler的select功能查看数据，返回True,data_list
    data_list = db_handler.select(
        date
    )
    return True, data_list


def year_income_interface(year):
    # 1.调用数据查看接口
    data_list = db_handler.select(
        year
    )

    data_dict = {
        '收入': 0,
        '支出': 0,
    }
    income = 0
    expenditure = 0

    for data in data_list:
        if 'a' in data[0]:
            income += float(data[2])
            data_dict['收入'] = income
        if 'b' in data[0]:
            expenditure += float(data[2])
            data_dict['支出'] = expenditure

    return True, data_dict