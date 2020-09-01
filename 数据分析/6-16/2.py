# -*- coding: utf-8 -*-

import requests
import re
import json
from pyecharts.charts import Bar
from pyecharts import options as opts

url1 = 'http://www.weather.com.cn/weather1d/101200101.shtml'# 武汉
url2 = 'http://www.weather.com.cn/weather1d/101270101.shtml' # 成都
url3 = 'http://www.weather.com.cn/weather1d/101230201.shtml' # 厦门
url4 = 'http://www.weather.com.cn/weather1d/101041800.shtml' # 巫溪

def get_data(url):
    res = requests.get(url=url)
    text = res.content.decode('utf-8')
    # print(text)
    r1 = re.findall('"od2":(.*])', text)
    r2 = r1[0]
    # 使用json把字符串转为字典
    r3 = json.loads(r2)
    today = r3
    print(today)
    return today

today1 = get_data(url1)  # 武汉相对湿度
today2 = get_data(url2)  # 成都相对湿度
today3 = get_data(url3)  # 厦门相对湿度

print([int(i['od27']) for i in today1])

c = (Bar()
     .add_xaxis([i['od21'] for i in today1])
     .add_yaxis('武汉',[int(i['od27']) if i['od27'] != 'null' else 0 for i in today1])
     .add_yaxis('成都',[int(i['od27']) if i['od27'] != 'null' else 0 for i in today2])
     .add_yaxis('厦门',[int(i['od27']) if i['od27'] != 'null' else 0 for i in today3])
     .set_global_opts(title_opts=opts.TitleOpts(title='过去24小时整点天气实况', subtitle='相对湿度'))
     )
c.render('html/2.html')



