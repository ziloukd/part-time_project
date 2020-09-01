# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
import os
import pandas as pd
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #解决中文乱码

def dataPreprocessing():
    # 读取数据
    df = pd.read_csv('28.bike_day.csv', encoding='utf-8-sig', header=0)
    # 查看前五行
    print(df.head(5))
    # 查看后两行
    print(df.tail(2))
    # 丢弃缺失值
    df = df.dropna()


def dataSelection():
    df = pd.read_csv('28.bike_day.csv', encoding='utf-8-sig', header=0)
    # 选择数据
    df_new = df.loc[:, ['instant', 'weathersit', 'casual', 'registered']]
    # 保存数据
    df_new.to_csv('bike_weathersit_user.txt', sep='\t', index=False)
    print('bike_weathersit_user.txt导出成功！')


def dataCalculate():
    # 读取txt数据
    df = pd.read_table('bike_weathersit_user.txt', sep='\t', header=0)
    # 计算数据
    df['cnt'] = df['casual'] + df['registered']
    # 导出数据
    df.to_excel('bike_weathersit_user_cnt.xlsx', sheet_name='sheet1', index=False)
    print('bike_weathersit_user_cnt.xlsx导出成功！')

def dataGroup():
    # 读数据
    df = pd.read_excel('bike_weathersit_user_cnt.xlsx', encoding='utf-8-sig', header=0)
    # 数据分组
    weathersit_group = df.groupby('weathersit')
    weathersit_mean = weathersit_group.mean()['cnt']
    # 数据保存
    weathersit_mean.to_csv('bike_weathersit_user_cnt_mean.txt', sep='\t')
    print('bike_weathersit_user_cnt_mean.txt导出成功！')

def dataVisualization():
    # 读取txt数据
    df = pd.read_table('bike_weathersit_user_cnt_mean.txt', sep='\t', header=0)
    x = list(df['weathersit'].values)
    y = list(df['cnt'].values)
    for i in range(1,5):
        if i not in x:
            x.insert(i - 1,i)
            y.insert(i -1, 0)

    # 画柱状图
    plt.bar(x,y,color='b')
    plt.xticks(x, ('Clear','Cloudy','lightRain','heavyRain'))
    plt.xlabel('天气')
    plt.ylabel('cnt')
    plt.legend(['cnt'])
    plt.savefig('bike_weathersit_user_cnt.png', dpi=400)
    plt.show()

def task():
    while True:
        menu()
        num = input('请输入任务选项：')
        if num == '1':
            dataPreprocessing()
        elif num == '2':
            if os.path.exists('28.bike_day.csv'):
                dataSelection()
 
            else:
                print('未能执行当前选项，请先执行前面的选项！')
        elif num == '3':
            if os.path.exists('bike_weathersit_user.txt'):
                dataCalculate()
            else:
                print('未能执行当前选项，请先执行前面的选项！')
        elif num == '4':
            if os.path.exists('bike_weathersit_user_cnt.xlsx'):
                dataGroup()
            else:
                print('未能执行当前选项，请先执行前面的选项！')
        elif num == '5':
            if os.path.exists('bike_weathersit_user_cnt_mean.txt'):
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
          '+--------共享单车租赁时天气数据分析及可视化系统----------+\n '
          '|0、退出。                                                  |\n'
          '|1、数据读取及预处理。                                       |\n'
          '|2、数据选择及导出。                                         |\n'
          '|3、数据计算。                                         |\n'
          '|4、数据统计分类。                                            |\n'
          '|5、数据可视化。                                              |\n'
          '|------------------------------------------------------------|')



if __name__ == '__main__':
    task()

