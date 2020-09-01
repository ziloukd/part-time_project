# -*- coding: utf-8 -*-
import os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif']=['SimHei'] #解决中文乱码

def dataPreprocessing():
    # 读取数据
    df = pd.read_csv('16.nao.long.data.csv', encoding='utf-8-sig', header=0)
    # 丢弃缺失值
    df = df.dropna()
    # 设置Year列为索引列
    df.set_index(['Year'], inplace=True)
    # 存储数据
    dic = {
        'Date':[],
        'NAO':[]
    }
    # 月份换算字典
    mon_dic = {1:'January', 2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    # 数据提取及处理
    for year in range(1824, 2019):
        for month in range(1, 13):
            NAO = df.loc[year, mon_dic[month]]
            if NAO == -99.99:
                NAO = -1
                print('3'*100)
            Date = '%d-%02d-01' % (year, month)
            dic['Date'].append(Date)
            dic['NAO'].append(NAO)
    # 数据写入及保存
    with open('nao_dropnan.txt', 'w', encoding='utf-8') as f1:
        f1.write('Date,NAO\n')
        for i in range(len(dic['Date'])):
            f1.write('{},{}\n'.format(dic['Date'][i], dic['NAO'][i]))
    print('nao_dropnan.txt导出成功！')

def datacalculate():
    dic = {
        'Date': [],
        'NAO': []
    }
    with open('nao_dropnan.txt', encoding= 'utf-8') as f1:
        row_list = f1.readlines()[1:]
        for row in row_list:
            Date, NAO = row.split(',')
            dic['Date'].append(Date)
            dic['NAO'].append(eval(NAO))

    df = pd.DataFrame(dic)
    return {'max':df.max()['NAO'],
            'min':df.min()['NAO'],
            'mean':df['NAO'].mean()}


def dataDescribe():
    dic1 = datacalculate()
    maxvalue = dic1['max']
    minvalue = dic1['min']
    dic = {
        'Date': [],
        'NAO': [],
        'label':[]
    }
    w_count = 0
    c_count = 0
    with open('nao_dropnan.txt', encoding='utf-8') as f1:
        row_list = f1.readlines()[1:]
        for row in row_list:
            Date, NAO = row.strip().split(',')
            dic['Date'].append(Date)
            dic['NAO'].append(eval(NAO))
            if 0 > eval(NAO) > minvalue:
                dic['label'].append('ColdRelate')
                c_count += 1
            else:
                dic['label'].append('WarmRelate')
                w_count += 1

    df = pd.DataFrame(dic)
    # 数据保存
    df.to_csv('nao_dropnan_result.csv', encoding='utf-8-sig', index=False)
    # print('nao_dropnan_result.csv导出成功！')

    labels = ['WarmRelate', 'ColdRelate']
    counts = [w_count, c_count]
    s = pd.Series(counts, index=labels)
    # 画饼图

    plt.axis('equal')
    plt.pie(s,
        labels = s.index,
        colors=['r','g'],
        autopct='%.2f%%',
        pctdistance=0.6,
        labeldistance=1.05,
        shadow=True,
        startangle=0,
        radius=1.5,
        frame=False
    )
    plt.savefig('nao_ pie.png', api=400)
    plt.show()

def dataVisualization():
    df = pd.read_csv('nao_dropnan_result.csv', header=0)
    df_NAO = df.loc[:, ['Date', 'NAO']]

    # 利用matplotlib画图
    plt.figure(figsize=(12,8))
    plt.plot(df_NAO['Date'],df_NAO['NAO'],label='NAO', color='blue')
    plt.xlabel('日期', fontsize=12)
    # 日期以年显示间隔为10
    xlength = len(df_NAO)
    # 构建xtickks显示位置
    xticksloc = [i for i in range(xlength) if i % 120 == 0]
    # 构建xticks显示标签
    xtickslabels = df_NAO['Date'].values[::120]
    # print(xtickslabels)
    plt.xticks(xticksloc, xtickslabels, rotation=90)
    plt.ylabel('NAO值', fontsize=12)
    plt.savefig('nao_dropnan_result.png', dpi=400)
    plt.show()
    print('任务4执行成功！')


def task():
    while True:
        menu()
        num = input('请输入任务选项：')
        if num == '1':
            dataPreprocessing()
        elif num == '2':
            if os.path.exists('nao_dropnan.txt'):
                res = datacalculate()
                print('NAO：')
                print('最大值:{},最小值:{},均值:{}'.format(res['max'], res['min'], res['mean']))
            else:
                print('未能执行当前选项，请先执行前面的选项！')
        elif num == '3':
            if os.path.exists('nao_dropnan.txt'):
                dataDescribe()
            else:
                print('未能执行当前选项，请先执行前面的选项！')
        elif num == '4':
            if os.path.exists('nao_dropnan_result.csv'):
                dataVisualization()
            else:
                print('未能执行当前选项，请先执行前面的选项！')
        elif num == '0':
            print('程序结束！')
            break
        else:
            print('输入选项有误')

def menu():
    print('【任务选择】\n'
          '+--------1824-2018 年北极涛动指数 NAO 数据分析及可视化系统----------+\n '
          '|0、退出。                                                  |\n'
          '|1、数据读取及预处理。                                       |\n'
          '|2、数据计算。                                         |\n'
          '|3、数据统计。                                               |\n'
          '|4、数据可视化。                                              |\n'
          '|------------------------------------------------------------|')



if __name__ == '__main__':
    task()

