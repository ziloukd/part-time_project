# -*- coding: utf-8 -*-
import pandas as pd

# 1、将Excel表格中的数据读取到python的二维列表中   （15分）
df = pd.read_excel(r'../requrests/Excel-房产销售.xlsx', header=1)
df.eval('房价总额 = 面积 * 单价', inplace=True)  # 添加新的一列房价总额

# 3、计算两室一厅和三室两厅两种户型的房子，分别售出多少套，以及平均单价，四舍五入取整   （15分）
output_quantity = df['户型'].value_counts()  # 两种户型的售出数信息：Name: 户型, dtype: int64

# .创建一个分组对象
group1 = df.groupby('户型')
# 算平均值
price_info = group1.mean()['单价']  # 两种户型的各自的平均单价：Name: 单价, dtype: float64

# 4、计算两室一厅和三室两厅两种户型的房子，分别最高和最低的总金额，四舍五入取整  （1round()
rp_max = {
    '两室一厅':round(df[df['户型'] == '两室一厅'].max()['房价总额']),
    '三室两厅':round(df[df['户型'] == '三室两厅'].max()['房价总额'])
}

rp_min = {
    '两室一厅':round(df[df['户型'] == '两室一厅'].min()['房价总额']),
    '三室两厅':round(df[df['户型'] == '三室两厅'].min()['房价总额'])
}

# 5、计算甲、乙、丙三个销售员分别售出多少套房子，以及销售总金额,四舍五入取整   （15分）
salesman_info = df['销售人员'].value_counts() # 销售员销售信息
group2 =df.groupby('销售人员')


print()


total_sales = group2.sum()['房价总额']  # 销售总金额

# 6、找出销售总金额最高的冠军销售员，售出房子数量最多的王牌销售员   （15分）
champion_salesman = total_sales.idxmax()  # 冠军销售员
ace_salesman = salesman_info.idxmax()  # 王牌销售员

# print(rp_max)
# 7、将分析结果以覆盖方式写入到txt文档，文档命名：学号_姓名.txt，和py文件在相同目录 （10分）
with open('学号_姓名.txt', 'w', encoding='utf-8') as f1:
    f1.write('学号：XX，姓名：XX，时间：XXXX-XX-XX XX:XX:XX\n')
    f1.write('------------------------\n')
    f1.write(f"两室一厅售出：{output_quantity['两室一厅']}套，平均单价：{round(price_info['两室一厅'])}元\n")
    f1.write(f"三室两厅售出：{output_quantity['三室两厅']}套，平均单价：{round(price_info['三室两厅'])}元\n")
    f1.write(f"两室一厅最高金额：{rp_max['两室一厅']}元，最低金额：{rp_min['两室一厅']}元\n")
    f1.write(f"三室两厅最高金额：{rp_max['三室两厅']}元，最低金额：{rp_min['三室两厅']}元\n")
    f1.write('------------------------\n')
    f1.write(f"人员甲 共售出房子 {salesman_info['人员甲']} 套，总销售额：{round(total_sales['人员甲'])}元\n")
    f1.write(f"人员乙 共售出房子 {salesman_info['人员乙']} 套，总销售额：{round(total_sales['人员乙'])}元\n")
    f1.write(f"人员丙 共售出房子 {salesman_info['人员丙']} 套，总销售额：{round(total_sales['人员丙'])}元\n")
    f1.write('------------------------\n')
    f1.write(f"冠军销售员：{champion_salesman}\n")
    f1.write(f"王牌销售员：{ace_salesman}\n")

