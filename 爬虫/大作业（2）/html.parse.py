# -*- coding: utf-8 -*-

import requests
import time
import re
from bs4 import BeautifulSoup
import csv
import jieba
import os


# 获取html页面
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'
    }
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    print(r.status_code)
    return r


# 使用html.parse解析器抓取正文
def parse(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    article = []  # 存储当前页面的所有正文
    p = soup.find_all('p')
    for line in p:
        text = line.string
        if text:
            article.append(text)
    return article

# 通过jieba精准分词，筛选出词频前10名
def participle_filter(text):
    words = jieba.lcut(text)
    # print(words)

    counts = {}
    # 去取单个汉字和非汉字部分
    for word in words:
        if not re.findall(r'[\u4e00-\u9fa5]+', word):
            continue
        if len(word) == 1:
            continue
        else:
            counts[word] = counts.get(word, 0) + 1
    # print(counts)
    items = list(counts.items())
    # 根据词频进行排序
    items.sort(key=lambda x:x[1], reverse=True)
    return items[:10]


# 处理的好结果保存到txt和csv文件中
def save(data):
    with open('result_html.parse/result.text', 'w', encoding='utf-8') as f1:
        f1.write(' 词语\t词频\n')
        for d in data:
            f1.write(f'{d[0]}\t{d[1]}\n')

    with open('result_html.parse/result.csv', 'w', encoding='utf-8') as f1:
        writer = csv.writer(f1)
        writer.writerow(['词语', '词频'])
        for d in data:
            writer.writerow(d)


def main():
    if os.path.exists('test.txt'):
        os.remove('test.txt')
    # 获取url
    with open('urls.text', encoding='utf-8') as f1:
        url_list = f1.read().split('|')

    for url in url_list:
        html = get_html(url.strip())
        text_list = parse(html)
        with open('test.txt', 'a', encoding='utf-8') as f1:
            print(len(text_list))
            for line in text_list:
                f1.write(line + '\n')

    with open('test.txt', encoding='utf-8') as f1:
        text = f1.read()

    res = participle_filter(text)
    save(res)

if __name__ == '__main__':
    start_t = time.time()
    main()
    end_t = time.time()
    print(f'总耗时：{end_t-start_t}')
