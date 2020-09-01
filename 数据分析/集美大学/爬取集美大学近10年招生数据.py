# -*- coding: utf-8 -*-
import csv
import requests
import traceback
from lxml import etree



url1 = 'http://zsb.jmu.edu.cn/info/1052/2902.htm'
url2 = 'http://zsb.jmu.edu.cn/info/1052/2542.htm'
url3 = 'http://zsb.jmu.edu.cn/info/1052/2230.htm'
url4 = 'http://zsb.jmu.edu.cn/info/1052/1017.htm'
url5 = 'http://zsb.jmu.edu.cn/info/1052/1019.htm'
url6 = 'http://zsb.jmu.edu.cn/info/1052/1022.htm'
url7 = 'http://zsb.jmu.edu.cn/info/1052/1024.htm'
url8 = 'http://zsb.jmu.edu.cn/info/1052/1026.htm'
url9 = 'http://zsb.jmu.edu.cn/info/1052/1028.htm'


def main():
    startSpider()
    
def startSpider():
    headers = {
	
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Cookie": "JSESSIONID=CA0AABA31ED1550F8D3AB7CE9911AEDE",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
	
	}
    url_dict = {'2019':url1,'2018':url2, '2017':url3, '2016':url4, '2015':url5,'2014':url6,'2013':url7,'2012':url8,'2011':url9}
    for k,v in url_dict.items():
        try:
            row_list = []
            result_data = []
            res = requests.get(url=v, headers=headers)
            html = etree.HTML(res.content.decode())
            if k=='2012':
                title_tr = html.xpath('//div[@id="vsb_content"]//table/tr[1]')[0]
                content_trs = html.xpath('//div[@id="vsb_content"]//table/tr[position()>1]')
    			
            else:
                title_tr = html.xpath('//div[@id="vsb_content"]//table/tbody/tr[1]')[0]
                content_trs = html.xpath('//div[@id="vsb_content"]//table/tbody/tr[position()>1]')
    
            for t in title_tr.xpath('./td'):
                row_list.append(''.join(t.xpath('.//text()')).strip())
            for c in content_trs:
                now_list = [''.join(i.xpath('.//text()')).strip()for i in c.xpath('./td')]
                result_data.append(now_list)
                # print(result_data)
            save_data(row_list, result_data, k)
        except:
            print(k, traceback.format_exc())
            
def save_data(title,content,file_name):
    file_name = "%s年集美大学招生录取分数.csv"%(file_name)
    print(title)
    with open(file_name,'w',newline='', encoding='utf-8-sig') as t:#numline是来控制空的行数的
        writer=csv.writer(t)#这一步是创建一个csv的写入器
        writer.writerow(title)#写入标签
        writer.writerows(content)#写入样本数据
        print('finished!')
    
if __name__=='__main__':
    main()