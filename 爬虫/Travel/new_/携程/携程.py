import aiohttp
import asyncio
import os
import re
import time
import json
from lxml import etree
from asyncio import Queue

class Common():
    start_url_queue= Queue()
    task_queue = Queue()
    picture_task_queue = Queue()
    CITY_PAGE_MAX = {}  # 各个城市，搜索结果的最终页面数
    CITY_LIST = ['武汉', '宜昌', '黄石', '十堰', '襄阳', '鄂州', '荆州', '荆门', '黄冈', '咸宁', '孝感', '随州', '恩施', '神农架','潜江', '天门', '仙桃']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    sem = asyncio.Semaphore(64)  # 控制并发数，增加稳定性

async def get_page_max():
    for city in Common.CITY_LIST:
        url = 'https://you.ctrip.com/searchsite/travels/?query=%s&isAnswered=&isRecommended=&publishDate=&PageNo=1'%city
        r, status = await asyncio.create_task(fetch(url, 'html'))
        tree = etree.HTML(r)
        page_max = tree.xpath("//div[@class='desNavigation cf']//a[contains(text(),'下一页')]/preceding-sibling::a[1]/text()")[0]  # 下一页的上一个元素
        Common.CITY_PAGE_MAX[city] = int(page_max)


async def fetch(url, flag):
    '''
    aiohttp获取网页源码
    '''
    async with Common.sem:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=Common.headers, verify_ssl=False) as resp:
                    if flag == 'html':
                        return await resp.text(), resp.status
                    if flag == 'json':
                        return await resp.json(), resp.status
                    if flag == 'content':
                        return await resp.read(), resp.status
            except Exception as e:
                return '超时',406

async def download_picture(queue):
    end_flag = True
    while end_flag:
        try:
            src, src_path, flag = queue.get_nowait()
        except:
            end_flag = False
            continue

        response,status = await loop.create_task(fetch(src, 'content'))
        for retry_time in range(3):
            if status == 200:
                break
            else:
                response, status = await asyncio.create_task(fetch(src, 'content'))
        if response == '超时':
            continue
        with open(src_path,'wb') as f1:
            f1.write(response)
        print(flag)

def sort_func(dic):
    # 日期转时间戳
    timeArray = time.strptime(dic['发表时间'], "%Y-%m-%d")
    # 轉換為時間戳:
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

async def get_and_parse(queue):
    end_flags = True
    while end_flags:
        try:
            data_info, file_path = queue.get_nowait()
            print('====',file_path)
        except:
            end_flags = False
            continue
        response, status = await asyncio.create_task(fetch(data_info['网址'], 'html'))
        for retry_time in range(3):
            if status == 200:
                break
            else:
                response, status = await asyncio.create_task(fetch(data_info['网址'], 'html'))

        # 解析
        ret = re.compile('<!-- 游记正文.*?-->(.*?)<!-- 游记正文.*? -->', re.S)
        html = ret.findall(response)[0]
        tree = etree.HTML(html)

        try:
            days_list = [i.strip() for i in tree.xpath("//span[contains(text(),'天数')]/text()")]
            data_info['天数'] = re.sub('天数：', '', '，'.join(days_list))
        except:
            pass

        try:
            time_list = [i.strip() for i in tree.xpath("//span[contains(text(),'时间')]/text()")]
            data_info['游玩时间'] = re.sub('时间：', '', '，'.join(time_list))
        except:
            pass

        try:
            costs_list = [i.strip() for i in tree.xpath("//span[contains(text(),'人均')]/text()")]
            data_info['人均'] = re.sub('人均：', '', '，'.join(costs_list))
        except:
            pass

        try:
            people_list = [i.strip() for i in tree.xpath("//span[contains(text(),'和谁')]/text()")]
            data_info['和谁'] = re.sub('和谁：', '', '，'.join(people_list))
        except:
            pass

        try:
            play_list = [i.strip() for i in tree.xpath("//span[contains(text(),'玩法')]/text()")]
            data_info['玩法'] = re.sub('玩法：', '', '，'.join(play_list))
        except:
            pass

        try:
            src_list = tree.xpath("//img/@data-original")
            data_info['src'] = src_list
        except:
            pass

        try:
            route_list = [i.strip() for i in tree.xpath("//dt[contains(text(),'作者去了这些地方')]/text()/../following-sibling::dd/a/text()")]
            data_info['旅游路线'] = '，'.join(route_list)
        except:
            pass

        try:
            content_list = tree.xpath('//p//text()')
            content = '\n'.join(i.strip() for i in content_list)
            data_info['正文'] = content

        except:
            print('da')
            pass

        try:
            id = tree.xpath("//a[@id='TitleFavourite']/@data-favouriteid")[0]
            commtent_url = 'https://you.ctrip.com/TravelSite/Home/TravelReplyListHtml?TravelId=%s' % id
            comment,status = await asyncio.create_task(fetch(commtent_url, 'json'))
            for retry_time in range(3):
                if status == 200:
                    break
                else:
                    comment, status = await asyncio.create_task(fetch(data_info['网址'], 'json'))
            Html = comment['Html']
            tree = etree.HTML(Html)
            comment_list = tree.xpath('//p[contains(@class, "ctd_comments_text")]/text()')
            comment = '\n'.join([str(index+1) + '.' + i.strip() for index,i in enumerate(comment_list)])
            data_info['评论'] = comment
            # print('#'*50)
            # print(comment)
            # print('#'*50)
        except:
            pass
        await asyncio.sleep(1)

        with open(file_path, 'r', encoding='utf-8') as f1:
            li = json.load(f1)
        li.append(data_info)
        temp_list = list(set([str(i) for i in li]))
        data_list = [eval(i) for i in temp_list]
        with open(file_path, 'w', encoding='utf-8') as f1:
            f1.write(json.dumps(data_list))
        print(data_info)

async def filter_and_save(queue):
    """
    提取出详情页的链接
    :param queue:
    :return:
    """
    end_flag = True
    while end_flag:
        try:
            url,city = queue.get_nowait()
            print(url)
        except:
            end_flag = False
            continue

        response, status = await asyncio.create_task(fetch(url, 'html'))
        for retry_time in range(3):
            if status == 200:
                break
            else:
                response, status = await asyncio.create_task(fetch(url, 'html'))

        # 选定范围
        ret = re.compile('<!-- 景点 -->(.*?)<!-- 底部搜索 -->',re.S)
        html = ret.findall(response)[0]
        tree = etree.HTML(html)
        li_list = tree.xpath('//li[@class="cf"]')
        data_info = {
            'city':'',
            '发表时间': '',
            '标题': '',
            '网址': '',
            '天数': '',
            '游玩时间': '',
            '人均': '',
            '和谁': '',
            '玩法': '',
            '旅游路线': '',
            '正文': '',
            '评论': '',
            'src':'',

        }  # 保存的结构
        for li in li_list:
            filter_request = li.xpath(".//dd[contains(@class,'color-999')]/text()")
            filter_request = ''.join(filter_request)
            if filter_request:
                date_time = re.findall('\d{4}-\d{1,2}-\d{1,2}', filter_request)[0]
                # 筛选在2017和2018年的攻略
                if '2018' in date_time or '2017' in date_time:
                    #date_time,headline,url
                    content_part_url = li.xpath('./a/@href')[0]
                    content_url = 'https://you.ctrip.com' + content_part_url
                    headline = li.xpath(f".//a[contains(@href,'{content_part_url}')]/text()")
                    headline = ''.join(headline).strip()

                    data_info['发表时间'] = date_time
                    data_info['网址'] = content_url
                    data_info['标题'] = headline
                    data_info['city'] = city

                    if '2017' in date_time:
                        json_path = '../2017/携程/%s/%s_new.json' % (city, city)
                    elif '2018' in date_time:
                        json_path = '../2018/携程/%s/%s_new.json' % (city, city)

                    with open(json_path, 'r', encoding='utf-8') as f1:
                        li = json.load(f1)
                    li.append(data_info)
                    # 去重
                    temp_list = list(set([str(i) for i in li]))
                    data_list = [eval(i) for i in temp_list]
                    with open(json_path, 'w', encoding='utf-8') as f1:
                        f1.write(json.dumps(data_list))
                    print(data_info)
                    # await Common.task_queue.put(data_info)


async def monitor_finish():
    while len(asyncio.Task.all_tasks()) > 1:
        await asyncio.sleep(1)
    await asyncio.sleep(5)
    raise SystemExit()

async def main():
    # # 第一步，爬取目录页，刷选详情的url
    # await get_page_max()  # 获取翻页阈值
    # await asyncio.sleep(2)  # 确保阈值已经拿到
    #
    # for city in Common.CITY_LIST:
    #     page = 1
    #     while 1:
    #         start_url = 'https://you.ctrip.com/searchsite/travels/?query=%s&isAnswered=&isRecommended=&publishDate=&PageNo=%d' % (city, page)
    #         await Common.start_url_queue.put((start_url, city))
    #         if page >= Common.CITY_PAGE_MAX[city]:
    #             break
    #         page += 1
    # print(Common.start_url_queue.qsize())
    # for _ in range(20):
    #     await loop.create_task(filter_and_save(Common.start_url_queue))
    #
    # 第二步， 请求详情页，将数据补充完整
    # for year in ('2017', '2018'):
    #     for city in Common.CITY_LIST:
    #         datafile_path = '../%s/携程/%s/%s.json' % (year,city,city)
    #         with open(datafile_path,encoding='utf-8') as f1:
    #             li = json.load(f1)
    #         # 去重，排序
    #         temp_list = list(set([str(i) for i in li]))
    #         data_list = [eval(i) for i in temp_list]
    #         data_list = sorted(data_list, key=lambda d:(d['发表时间'],d['标题']))  # 时间有相同，以时间为主标题为辅
    #         if not data_list:
    #             continue
    #         for data in data_list:
    #             save_path = '../%s/携程/%s/%s_new.json' % (year,city,city)
    #             await Common.task_queue.put((data,save_path))
    # # 下载详情数据
    # for _ in range(6):
    #     loop.create_task(get_and_parse(Common.task_queue))

    # # 第三步下载图片
    # for year in ('2017', '2018'):
    #     if year == '2017':
    #         continue
    #     for city in Common.CITY_LIST:
    #         datafile_path = '../%s/携程/%s/%s_new.json' % (year,city,city)
    #         with open(datafile_path,encoding='utf-8') as f1:
    #             li = json.load(f1)
    #         # 去重，排序
    #         temp_list = list(set([str(i) for i in li]))
    #         data_list = [eval(i) for i in temp_list]
    #         if not data_list:
    #             continue
    #         data_list = sorted(data_list, key=sort_func)
    #         for data_num, data in enumerate(data_list):
    #             if not data['src']:
    #                 continue
    #             for src_num, src in enumerate(data['src']):
    #                 if city in ('武汉', '宜昌', '黄石', '十堰', '襄阳', '鄂州', '荆州', '荆门', '黄冈', '咸宁', '孝感', '随州', '恩施', '神农架','潜江', '天门'):
    #                     continue
    #                 if src_num > 200:
    #                     continue
    #                 src_name = '%d-%s-图片%d.jpg' % (data_num + 1, data['标题'], src_num + 1)
    #                 src_name = re.sub(r'[|*:"?<>\\/\u3000\s]','', src_name)
    #                 picture_save_catalog = '../%s/携程/%s/images'% (year,city)
    #                 if not os.path.exists(picture_save_catalog):
    #                     os.makedirs(picture_save_catalog)
    #                 src_path = os.path.join(picture_save_catalog, src_name)
    #                 flag = 'procession --> %s--%s--%sS' % (data['发表时间'], city, src_name)
    #                 await Common.picture_task_queue.put((src,src_path,flag))
    # #下载图片
    # for _ in range(50):
    #     loop.create_task(download_picture(Common.picture_task_queue))

    # 去哪儿的图片下载也可以用这个
    for year in ('2017', '2018'):
        if year == '2017':
            continue
        for city in Common.CITY_LIST:
            datafile_path = '../%s/去哪儿/%s/%s_new.json' % (year,city,city)
            with open(datafile_path,encoding='utf-8') as f1:
                li = json.load(f1)
            # 去重，排序
            temp_list = list(set([str(i) for i in li]))
            data_list = [eval(i) for i in temp_list]
            if not data_list:
                continue
            data_list = sorted(data_list, key=sort_func)
            for data_num, data in enumerate(data_list):
                if not data['src_url']:
                    continue
                for src_num, src in enumerate(data['src_url']):
                    if city == '武汉':
                        continue
                    if src_num > 200:  # 偷个懒
                        continue
                    src_name = '%d-%s-图片%d.jpg' % (data_num + 1, data['标题'], src_num + 1)
                    src_name = re.sub(r'[|:"?*<>\\/\u3000\s]','', src_name)
                    picture_save_catalog = '../%s/去哪儿/%s/images'% (year,city)
                    if not os.path.exists(picture_save_catalog):
                        os.makedirs(picture_save_catalog)
                    src_path = os.path.join(picture_save_catalog, src_name)
                    flag = 'procession --> %s--%s--%sS' % (data['发表时间'], city, src_name)
                    await Common.picture_task_queue.put((src,src_path,flag))
    #下载图片
    for _ in range(50):
        loop.create_task(download_picture(Common.picture_task_queue))
    loop.create_task(monitor_finish())




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()





