import requests
from lxml import etree
import re
import csv
import os


class doubanMovies:
    #headers 头部信息
    #allDataList 存储所有信息的二维列表，
    def __init__(self,headers,allDataList):
        self.headers = headers
        self.allDataList = allDataList

    #爬取电影信息
    def getMoviesInfo(self,pageUrl,i):

        html = requests.request('get', url=pageUrl, headers=headers)
        # 设置网页编码格式
        html.encoding = 'utf8'
        text = html.text
        tree = etree.HTML(text)

        items = tree.xpath('//ol/li/div/div[@class="info"]')

        for item in items:
            #电影名
            name = item.xpath("./div[@class= 'hd']/a/span[1]/text()")[0]
            #电影别名
            otherName = item.xpath("./div[@class='hd']/a/span[@class='other']/text()")
            #过滤后的电影别名
            clean_OtherName = otherName[0].split('/',1)[1].replace('  ',"").lstrip()
            #导演各种信息
            bd_info = item.xpath("./div[@class='bd']/p[1]/text()")#返回一个列表
            #导演
            director = bd_info[0].replace("\n", "").split('   ')
            clean_director = director[0].split(':')[1].strip()

            info_1 = bd_info[1].strip().replace("\n", "").split(' / ')
            #年份
            year = info_1[0].strip()
            #国家
            country = info_1[1].strip()
            #类型
            type = info_1[2].strip()
            #评分
            rating = item.xpath("./div[@class='bd']/div[@class='star']/span[2]/text()")[0]
            #评分人数
            evaluation_num = item.xpath("./div[@class='bd']/div[@class='star']/span[4]/text()")
            clean_evaluation_num =re.findall(r'\d+',evaluation_num[0])[0]
            #一句话简介
            quote_tag = item.xpath("./div[@class='bd']/p/span[@class='inq']")
            # 注意可能可能没有quote简评
            if len(quote_tag) is not 0:
                quote = quote_tag[0].text
            else:
                quote=""

            list = [i,name,clean_OtherName,clean_director,year,country,type,rating,clean_evaluation_num,quote]
            i = i+1
            allDataList.append(list)


    def getPageUrl(self):
        for i in range(0,250,25):
            Pageurl = "https://movie.douban.com/top250?start={}&filter=".format(i)
            print(Pageurl)
            movies.getMoviesInfo(Pageurl,i+1)

    #将数据写入csv文件
    def writeToCsv(self,allDataList):
        print(getCurRunPosInfo())
        path = r'./data/'
        if not os.path.exists(path):
            os.mkdir(path)

        with open(path+"movies.csv","w",encoding='utf8',newline="") as csvfile:
            writer = csv.writer(csvfile)
            #列名
            writer.writerow(['Top250','MovieName', 'OtherName', 'Director',
                             'Year', 'Country', 'Type', 'Rating', 'EvaluationNum',
                             'quote'])
            writer.writerows(allDataList)

    #main方法
    def main(self,allDataList):
        movies.getPageUrl()
        movies.writeToCsv(allDataList)



def getCurRunPosInfo():
    import sys
    try:
        raise Exception
    except:
        exc_info = sys.exc_info()
        traceObj = exc_info[2]
        frameObj = traceObj.tb_frame
        #print frameObj.f_code.co_name,frameObj.f_lineno
        Upframe = frameObj.f_back
        #print Upframe.f_code.co_name, Upframe.f_lineno
        return (Upframe.f_code.co_filename, Upframe.f_code.co_name, Upframe.f_lineno)

# 头部信息
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

allDataList = []
movies = doubanMovies(headers,allDataList)
movies.main(allDataList)
