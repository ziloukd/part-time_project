# -*- coding: utf-8 -*-
# @Time : 2020/6/12 8:33
# @Author : XX
# @File : 多城市天气预报.py
# @Software: PyCharm
# 推荐安装pyecharts1.6.0
# pip install pyecharts==1.6.0
# 如果使用pycharm安装，settings中project中 project interpreter点击，
# 点击右方加号，搜索pyecharts点击install即可。
# 如果要指定版本，勾选右下方specify version，选择1.6.0
# 然后在点击install package
# 如果安装成功后，发现版本不对，卸载重装
# 卸载:pip uninstall pyecharts

import requests
import re
import json
from pyecharts.charts import Bar
from pyecharts import options as opts

url1 = 'http://www.pm25.in/guangzhou'# 广州
url2 = 'http://www.pm25.in/shanghai' # 上海
url3 = 'http://www.pm25.in/tianjin' # 天津

def get_data(url):
    res = requests.get(url=url)
    text = res.content.decode('utf-8')
    # print(text)
    r1 = re.findall('categories: (.*?])', text)
    r2 = re.findall('data: (\[.*?])', text)
    print(r1, r2)
    # 使用json把字符串转为字典
    xAsis = json.loads(r1[0])
    yAsis = json.loads(r2[0])
    return xAsis, yAsis

today1 = get_data(url1)
today2 = get_data(url2)
today3 = get_data(url3)

c = (Bar()
     .add_xaxis([i for i in today1[0]])
     .add_yaxis('广州',[int(i) for i in today1[1]])
     .add_yaxis('上海',[int(i) for i in today2[1]])
     .add_yaxis('天津',[int(i) for i in today3[1]])
     .set_global_opts(title_opts=opts.TitleOpts(title='城市最近24小时空气质量指数', subtitle=''))
     )
c.render('html/1.html')

