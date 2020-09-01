#-*- coding: utf-8 -*-
"""1.分析集美大学各省2011年-2019年本一批理工平均分数，并使用柱状图展示排名top10
2.分析集美大学各省2011-2019年各批次文史平均分变化趋势，使用折线图展示结果
3.分析集美大学各省2016-2019年录取人数分布"""

import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体

def open_and_deal_data():
#遍历csv文件并打开
    df_list = []
    for i in range(1,10):
        path="201{}年集美大学招生录取分数.csv".format(i)
        df=pd.read_csv(path, header=0)  #header=0表示有标题行
        # 1.分析集美大学各省2011年-2019年本一批理工平均分数，并使用柱状图展示排名top10
        temp = df.loc[:,['省份','批次','科类', '平均分']] # 选择需要的数据类型
        temp1 = temp[(temp['批次'] == '本一批') & (df['科类'] == '理工')]  # 筛选需要的数据
        res = temp1.sort_values('平均分', ascending=False) # 按平均分降序排序
        
        title_1 = "201{}年集美大学各省份本一批理工平均分排名".format(i)
        print(title_1)
        print(res)
        plot_bar(res['省份'][:10], res['平均分'][:10], title_1)  # 调用plot_bar画柱状图

        # 2.预处理
        df['年份'] = int('201{}'.format(i))
        df_list.append(df)

    # 2.分析集美大学各省2011-2019年各批次文史平均分变化趋势，使用折线图展示结果
    new_dataframe = df_list[0].append(df_list[1:])
    temp = new_dataframe.loc[:,['省份','批次','科类', '平均分','录取人数', '年份']] # 选择需要的数据类型
    temp2 = temp[(temp['科类'] == '文史') & (temp['省份'] == '四川')]  # 筛选需要的数据
    groups = temp2.groupby('批次')  # 按批次分组
    for group in groups:
        res = group[1].sort_values('年份')  # 按照年份排序
        title = '{}{}平均分变化趋势'.format('四川', group[0])
        print(title)
        plot_line(res, title)
            #
    # 3.分析集美大学四川省2017-2019年各批次录取人数分布
        temp = group[1][group[1]['年份'] > 2016]
        title = "集美大学四川省2017-2019年{}录取人数分布".format(group[0])
        print(title)
        print(temp)

        plot_bar(temp['年份'], temp['录取人数'], title = title)

# 数据可视化之柱状图
def plot_bar(x, y, title):
    plt.bar(
        range(len(y)),
        y,
        tick_label = x,
    )
    plt.xticks(rotation=90)
    plt.figsize = (12,8)
    plt.title(title)
    plt.show()

# 数据可视化之折线图
def plot_line(res, title):
    res.年份=pd.to_numeric(res.年份)
    res.平均分=pd.to_numeric(res.平均分)
    print(res)

    res.plot(
        kind = 'line',
        x = '年份',
        y = '平均分'
    )
    plt.title(title)
    plt.show()


open_and_deal_data()   


    
        
    
