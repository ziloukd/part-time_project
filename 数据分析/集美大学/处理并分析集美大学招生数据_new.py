# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 17:57:58 2020

@author: lwy
"""
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
import numpy as np

mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体


class Jimei():
    def __init__(self, debug=False):
        self.debug = debug
    
    def open_and_deal_data(self):
        
        # 构建合并表数据结构
        path="2011年集美大学招生录取分数.csv"
        df0=pd.read_csv(path, header=0)  #header=0表示有标题行
        df0['录取人数'] = 'NaN'
        temp_df0 = df0.loc[:,['省份','批次','科类','录取人数','平均分']]
        temp_df0['年份'] = 2011
        
        df_list = []
        
        for i in range(2,10):
            path="201{}年集美大学招生录取分数.csv".format(i)
            df=pd.read_csv(path, header=0)  #header=0表示有标题行
            try:
                temp = df.loc[:,['省份','批次','科类','录取人数','平均分']] # 选择需要的数据类型
            except KeyError:
                df['录取人数'] = 'NaN'
                temp = df.loc[:,['省份','批次','科类','录取人数','平均分']]
            temp['年份'] = int('201{}'.format(i))
            df_list.append(temp)
        self.df = temp_df0.append(df_list)  # 合并表数据
        
        if self.debug:
            print(self.df)
     
    # 1.分析集美大学各省2011年-2019年本一批理工平均分数TOP10          
    def get_Top10(self, year):
        self.open_and_deal_data()
        temp = self.df[(self.df['批次'] == '本一批') & (self.df['科类'] == '理工')\
                       & (self.df['年份'] == year)]
        res = temp.sort_values('平均分', ascending = False)[:10]
        # print(res)
        # 画柱状图
        res.平均分=pd.to_numeric(res.平均分)
        try:
            res.plot(kind = 'bar', x = '省份', y = '平均分', color = 'c',
                     title = '集美大学{}本一批理工平均分数TOP10'.format(year),
                     rot = 0, figsize = (8, 6))
            plt.xlabel('省份')
            plt.ylabel('平均分')
            plt.show()
        except IndexError:
            print('{}没有本一批理工数据'.format(year))
            
    #2.分析集美大学四川省2011-2019年各批次文史平均分变化趋势     
    def get_average_trends(self):
        self.open_and_deal_data()
        df = self.df[(self.df['省份'] == '四川') & (self.df['科类'] == '文史')]
        groups = df.groupby('批次')
        for i, group in enumerate(groups):
            print(i + 1, group[0])
        while True:
            try:
                user_choice = input('输入批次序号查看该批次文史平均变化趋势(输入0查看所有,\
                                    直接确认退出查看):').strip()
                if not user_choice:
                    break
                else:
                    user_choice = int(user_choice)
            except:
                print('输入不合法！')
                continue
            
            
            
            if user_choice not in range(1,len(groups) + 1) and user_choice != 0:
                print('没有该批次的数据')
                continue
            
            for i, group in enumerate(groups):
                if user_choice == 0:
                    pass
                elif user_choice == i+1:
                    pass
                else:
                    continue
                res = group[1].sort_values('年份')
                
                # 画图
                res.年份=pd.to_numeric(res.年份)
                res.平均分=pd.to_numeric(res.平均分)
                res.plot(
                    kind = 'line',
                    x = '年份',
                    y = '平均分',
                    title = '集美大学四川省2{}文史平均分变化趋势'.format(group[0]),
                    color = 'c',
                    rot = 0,
                    figsize = (12,8))
                plt.xlabel('年份')
                plt.ylabel('平均分')
                plt.show()
        
    # 3.分析集美大学四川省2017-2019年各批次录取人数分布
    def get_admissions_distribution(self):
        self.open_and_deal_data()
        df = self.df[(self.df['省份'] == '四川') & (self.df['年份'] > 2016)]
        groups = df.groupby('批次')


        x_tags = ['2017','2018','2019']
        x = np.arange(3)
        total_width, n = 0.8, len(groups)
        width = total_width / n
        
        color_list = ['yellow','red','green','orange','blue']
        
        for i, group in enumerate(groups):
            
            temp = group[1].groupby('年份').sum()
            temp['年'] = temp.index
            temp = temp.loc[:, ['年', '录取人数']]
            for j in range(2017,2020):
                if not j in temp['年']:
                    temp.loc[j] = [j, 0]
            res = temp.sort_values('年')
            print(res)
             # 画图
            plt.bar(x + width*i, res['录取人数'].values, width=width, label = group[0],
                    fc = color_list[i], tick_label = x_tags)
        plt.xlabel('年份')
        plt.ylabel('录取人数')
        plt.title('集美大学四川省2017-2019年各批次录取人数分布')
        plt.legend()
        plt.show()
        
def main():
    object1 = Jimei()
    while True:
        print("""
              a.分析集美大学各省2011年-2019年本一批理工平均分数TOP10 
              b.分析集美大学四川省2011-2019年各批次文史平均分变化趋势
              c.分析集美大学四川省2017-2019年各批次录取人数分布""")
              
        user_choice = input('输入序号(直接确认可退出):').strip()
        
        if not user_choice:
            break
        
        if user_choice == 'a':
            for i in range(2011, 2020):
                object1.get_Top10(i)
                
        elif user_choice == 'b':   
            object1.get_average_trends()
            
        elif user_choice == 'c':
            object1.get_admissions_distribution()
            
        else:
            print('输入不合法')

if __name__ == '__main__':
    main()
    