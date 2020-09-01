import pandas as pd
# 导入数据
df = pd.read_csv('tourist_statistic.csv', header=0) # header=0表示有标题行

# (2)
temp = df.loc[:, '2009年':'2018年']
df['平均入境游客(万人次)'] = temp.mean(axis=1, ).map(lambda x:('%.4f') % x) # axis 0为列　１为行
print(df)
print('**************')


# (3)
asia = df[(df['所属洲'] == '亚洲')&(df['2018年'] > 180)]
print(asia['指标(万人次)'])
print('**************')


# (4)
temp4 = df[(df['所属洲'] == '欧洲')&(df['指标(万人次)'] == '俄罗斯入境游客')]
rating = (temp4['2018年'] - temp4['2009年']) / temp4['2009年']
print('增长率:',rating)
print('**************')


# (5)
total_people = temp.sum(axis=0)
print(total_people)
print('**************')


# (6)
temp6 = df.loc[:,['所属洲', '2010年', '2014年', '2018年']]
group1 = temp6.groupby('所属洲')
total = group1.sum()
print(total)
print('**************')

# (7)
tem7 = total.sort_values('2018年', ascending=False)
print(tem7)