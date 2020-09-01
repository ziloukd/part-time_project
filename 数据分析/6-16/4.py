# -*- coding: utf-8 -*-


import requests
import re
from pyecharts.charts import Bar
from pyecharts import options as opts

url1 = 'https://www.weaoo.com/huangshi-181583.html'# 黄石
url2 = 'https://www.weaoo.com/ezhou-181520.html' # 鄂州


def get_data(url):
    res = requests.get(url=url)
    text = res.content.decode('utf-8')
    # print(text)
    r1 = re.findall('<li>\n<span>(\d{2}?点)</span>.*?<span>(\d{2}?℃).*?</li>', text, re.S)
    # print(r1)
    return r1

today1 = get_data(url1)
today2 = get_data(url2)


c = (Bar()
     .add_xaxis([i[0] for i in today1])
     .add_yaxis('黄石',[int(i[1].strip('℃')) for i in today1])
     .add_yaxis('鄂州',[int(i[1].strip('℃')) for i in today2])
     .set_global_opts(title_opts=opts.TitleOpts(title='城市未来二十四小时温度预报', subtitle=''))
     )
c.render('html/4.html')
