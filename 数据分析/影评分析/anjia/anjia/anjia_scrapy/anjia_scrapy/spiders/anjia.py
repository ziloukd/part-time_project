# -*- coding: utf-8 -*-
import scrapy
import requests
import re
from scrapy.conf import settings
from ..items import AnjiaItem

class AnjiaSpider(scrapy.Spider):
    name = 'anjia'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/subject/30482003/reviews?sort=time&start=0']

    def parse(self, response):
        # 获取评论标签列表
        review_list = response.xpath("//div[contains(@class,'review-list')]/div")
        for review_div in review_list:
            # 作者
            author = review_div.xpath(".//a[@class='name']/text()").get()
            # 发布时间
            pub_time = review_div.xpath(".//span[@class='main-meta']/text()").get()
            # 评分
            rating = review_div.xpath(".//span[contains(@class,'main-title-rating')]/@title").get() or ""
            # 标题
            title = review_div.xpath(".//div[@class='main-bd']/h2/a/text()").get()

            # 是否有展开按钮
            is_unfold = review_div.xpath(".//a[@class='unfold']")
            if is_unfold:
                # 获取评论id
                review_id = review_div.xpath(".//div[@class='review-short']/@data-rid").get()
                # 获取内容
                content = self.get_fold_content(review_id)
            else:
                content = review_div.xpath(".//div[@class='main-bd']//div[@class='short-content']/text()").get()
            if content:
                content = re.sub(r"\s",'',content)
            # 创建item对象
            item = AnjiaItem(
                author=author,
                pub_time=pub_time,
                rating=rating,
                title=title,
                content=content
            )
            yield item
        # 如果有下一页
        next_url = response.xpath("//span[@class='next']/a/@href").get()
        if next_url:
            # 请求下一页的数据
            yield scrapy.Request(response.urljoin(next_url),self.parse)

    def get_fold_content(self,review_id):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
        url = "https://movie.douban.com/j/review/{}/full".format(review_id)
        resp = requests.get(url,headers=headers)
        data = resp.json()
        content = data['html']
        content = re.sub(r"(<.+?>)","",content)
        return content



