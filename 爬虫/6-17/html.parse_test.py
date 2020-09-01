# -*- coding: utf-8 -*-

import requests
import time
import re
from bs4 import BeautifulSoup
import csv
import jieba
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

# 获取html页面
def get_html(url):
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    print(r.status_code)
    return r


# 使用html.parse解析器抓取正文
def get_text(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    article = []  # 存储当前页面的所有正文
    p = soup.find_all('p')
    for line in p:
        text = line.string
        if text:
            article.append(text)
    return article

# 通过jieba精准分词，筛选出词频前10名
def participle_and_filter(text):
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
    with open('urls.text', encoding='utf-8') as f1:
        url_list = f1.read().split('|')

    for url in url_list:
        html = get_html(url.strip())
        text_list = get_text(html)
        with open('test.txt', 'a', encoding='utf-8') as f1:
            print(len(text_list))
            for line in text_list:
                f1.write(line + '\n')

    with open('test.txt', encoding='utf-8') as f1:
        text = f1.read()

    res = participle_and_filter(text)
    save(res)

if __name__ == '__main__':
    start_t = time.time()
    if os.path.exists('test.txt'):
        os.remove('test.txt')
    main()
    end_t = time.time()
    print(f'总耗时：{end_t-start_t}')
    # response = get_html('https://www.voachinese.com/a/covid-new-study-20200617/5465866.html')
    # get_text(response)