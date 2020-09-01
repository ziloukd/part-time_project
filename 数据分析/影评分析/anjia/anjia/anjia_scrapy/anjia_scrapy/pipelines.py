# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class AnjiaScrapyPipeline(object):
    def __init__(self):
        self.fp = open("reviews.json", 'w', encoding='utf-8')

    def process_item(self, item, spider):
        self.fp.write(json.dumps(dict(item))+"\n")
        return item

    def close_spider(self,spider):
        self.fp.close()
