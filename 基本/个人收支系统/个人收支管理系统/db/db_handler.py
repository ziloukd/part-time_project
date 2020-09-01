# -*- coding: utf-8 -*-
'''数据处理层'''
import csv, os
from common import setting


def save(data):
    # 保存数据
    file_path = os.path.join(
        setting.DB_PATH, '个人收支信息.csv'
    )
    f = open(file_path, mode="a+", newline="", encoding="utf-8-sig")
    csv_write = csv.writer(f)
    csv_write.writerow(data.split(','))
    f.close()


def select(date):
    # 查看数据
    file_path = os.path.join(
        setting.DB_PATH, '个人收支信息.csv'
    )
    f = open(file_path,encoding="utf-8-sig")
    csv_reader = csv.reader(f)
    for row in csv_reader:
        if date in row[1]:
            yield row
    f.close()