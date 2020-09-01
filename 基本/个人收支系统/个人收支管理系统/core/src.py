# -*- coding: utf-8 -*-
'''用户视图层'''
from interface import user_interface
from common import setting


def income_and_expenditure():
    print('收入类：', end=' ')
    for item in setting.income_dict.items():
        print('%s-%s' % item, end=' ')
    print()
    print('支出类：', end=' ')

    for item in setting.expenditure_dict.items():
        print('%s-%s' % item, end=' ')
    print()

    print('请逐笔输⼊类别编码、发⽣⽇期、⾦额、备注（各数据⽤英⽂逗号分隔,直接输⼊回⻋表示输⼊结束）')

    while True:

        detail = input('输入其他任意继续，直接确认退出：').strip()

        if not detail:
            break

        # 调用db_handler接口的数据写入功能
        flag, msg = user_interface.detail_save_interface(
            detail
        )

        if flag:
            print(msg)
        else:
            print(msg)


def query_month_bill():
    while True:
        date = input('请输入对收支类别数据进行汇总的月份:').strip()

        # 调用user_interface的汇总查看功能
        flag, msg = user_interface.summary_view_interface(
            date
        )

        # 输出数据
        print("收入/支出", '\t', '明细类别', '\t', '金额')
        for data in msg.items():
            if 'a' in data[0]:
                print("收入", '\t', setting.income_dict.get(data[0]), '\t', data[1])
            if 'b' in data[0]:
                print("支出", '\t', setting.expenditure_dict.get(data[0]), '\t', data[1])
        print(f'{date}的总收入为:{msg["收入"]}\t总支出为:{msg["支出"]}')
        if flag:
            pass
        else:
            print(msg)
            continue

        # 选择是否输出该月的各笔明细
        choice = input('输入y查看明细，输入其他任意退出查看账单功能：').strip()
        if choice.lower() != 'y':
            break

        # 调用user_interface的查看明细功能
        flag, msg = user_interface.detail_view_interface(
            date
        )

        print('\n' + '类别' + '\t' + '收入/支出' + '\t' + '发生日期' + '\t' + '金额' + '\t' + '备注')
        for row in msg:
            if ('a' in row[0]):
                print(row[3] + '\t' + '收入' + '\t' + row[1] + '\t' + str(row[2]))
            else:
                print(row[3] + '\t' + '支出' + '\t' + row[1] + '\t' + str(row[2]))

        if flag:
            pass
        else:
            print(msg)

        r = input('输入y退出，输入其他任意继续：').strip()

        if r.lower() == 'y':
            break


def year_income():
    while True:
        year = input('请输入查询的年份：').strip()

        # 调用年统计功能
        flag, msg = user_interface.year_income_interface(
            year
        )

        print(f'{year}年：年总支出：{msg["收入"]}，年总支出:{msg["支出"]}')

        if flag:
            pass
        else:
            print(msg)
            continue

        r = input('输入y退出，输入其他任意继续：').strip()

        if r.lower() == 'y':
            break

func_dict = {
    '1': income_and_expenditure,
    '2': query_month_bill,
    '3': year_income,
}

def run():
    while True:
        print(
            '''
            ============欢迎使用[个人收支管理系统]============
            
                            1.写入收支明细
                            2.查询月账单
                            3.年账单汇总
                                               
            ======================end======================
            '''
        )

        choice = input('请输入功能编号：').strip()

        if choice not in func_dict:
            print('输入有误！')
            continue

        func_dict.get(choice)()

        flag = input('是否确认退出系统(输入y退出，输入其他任意继续)：').strip()

        if flag.lower() == 'y':
            break