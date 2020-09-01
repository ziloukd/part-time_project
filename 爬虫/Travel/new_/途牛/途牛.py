import aiohttp
import asyncio
import os
import re
import json
from lxml import etree
from asyncio import Queue

class Common():
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    task_queue = Queue()
    picture_task_queue = Queue()
    start_url_queue = Queue()
    page_queue = Queue()
    CITY_LIST = ['武汉', '宜昌', '黄石', '十堰', '襄阳', '鄂州', '荆州', '荆门', '黄冈', '咸宁', '孝感', '随州', '恩施', ]

async def fetch(queue):
    while 1:
        url,src_path,flag = queue.get_nowait()
        # print(url)
        async with aiohttp.ClientSession() as session:
            try:
                html = await session.get(url, timeout=3)
                content = await html.read()
                print(flag,'status:%d' % html.status)
                with open(src_path, 'wb') as f1:
                    f1.write(content)
            except:
                pass
        queue.task_done()

async def get_html(url, type):
    async with aiohttp.ClientSession() as session:
        """发起请求，根据不同的需求，返回text或文本"""
        try:
            response = await session.get(url, headers=Common.headers, timeout=10)
        except asyncio.exceptions.TimeoutError as e:
            return '超时', 404
        if type == 'html':
            return await response.text(), response.status
        if type == 'json':
            return await response.json(), response.status
        if type == 'content':
            return await response.read(), response.status

async def get_and_parse(queue):
    end_flag =True
    while end_flag:
        try:
            data_info, json_path = queue.get_nowait()
            print('ji哪里了e')
        except:
            end_flag = False
            continue

        url = data_info['网址']
        html, status = await asyncio.create_task(get_html(url, 'html'))
        #
        for retry_time in range(3):
            if status == 200:
                break
            else:
                await asyncio.sleep(0.2)
                html, status = await asyncio.create_task(get_html(url, 'html'))


        # 解析
        tree = etree.HTML(html)
        try:
            play_list = [i.strip() for i in tree.xpath("//div[@class='tag-item']/text()")]
            data_info['玩法'] = re.sub('#', '', '，'.join(play_list))
            # print(data_info['玩法'])
        except:
            pass

        try:
            content_list = tree.xpath("//div[contains(@class, 'sdk-trips-text')]//text()")
            content = '\n'.join(i.strip() for i in content_list)
            data_info['正文'] = content

        except:
            pass

        try:
            src_list = tree.xpath("//img/@data-src")
            data_info['src'] = src_list
        except:
            pass

        try:
            id = re.findall('https://www.tuniu.com/trips/(\d+)', url)[0]
            commtent_url = 'https://www.tuniu.com/web-community/api/travel/getCommentList?d={"targetType":1008,"targetId":%s}&c={"ct":100}' % id
            # print(commtent_url)
            comment = await get_html(commtent_url, 'json')
            comment_list = comment['data']['contentInfoForSdks']
            comment = '\n'.join([str(index+1) + '.' + i['commentText'].strip() for index,i in enumerate(comment_list)])
            data_info['评论'] = comment
        except:
            # print(1)
            pass
        await asyncio.sleep(1)

        #
        with open(json_path, 'r', encoding='utf-8') as f1:
            li = json.load(f1)
        li.append(data_info)
        temp_list = list(set([str(i) for i in li]))
        li = [eval(i) for i in temp_list]
        with open(json_path, 'w', encoding='utf-8') as f1:
            f1.write(json.dumps(li))
        print(data_info)

async def get_api_link(queue):
    end_flag = True
    while end_flag:
        try:
            url, city = queue.get_nowait()
            # print(url)
        except:
            end_flag = False
            continue

        #
        json_response, status = await asyncio.create_task(get_html(url, 'json'))
        #
        for retry_time in range(3):
            if status == 200:
                break
            else:
                await asyncio.sleep(0.2)
                json_response, status = await asyncio.create_task(get_html(url, 'json'))
        page_num = 1
        while 1:
            page_num += 1
            start_url = 'https://trips.tuniu.com/travels/index/ajax-list?queryKey=%s&page=%d' % (city,page_num)
            # print(start_url)
            await Common.page_queue.put((start_url,city))
            if page_num >+ json_response['data']['pageCount']:
                break

async def filter_and_get_url(queue):
    end_flag = True
    while end_flag:
        try:
            url, city = queue.get_nowait()
            # print(url)
        except:
            end_flag = False
            continue

        #
        json_response, status = await asyncio.create_task(get_html(url, 'json'))
        #
        for retry_time in range(3):
            if status == 200:
                break
            else:
                await asyncio.sleep(0.2)
                json_response, status = await asyncio.create_task(get_html(url, 'json'))
        # 数据结构
        data_info = {
            'city': '',
            '标题': '',
            '网址': '',
            '发表时间': '',
            '天数': '',
            '游玩时间': '',
            '人均花费': '',
            '和谁': '',
            '玩法': '',
            '旅游路线': '',
            '正文': '',
            '评论': '',

        }
        # 筛选符合条件的数据
        for data in json_response['data']['rows']:
            # print(data['publishTime'],city)
            if '2017' in data['publishTime'] or '2018' in data['publishTime']:
                data_info['city'] = city
                data_info['标题'] = data['name']
                data_info['发表时间'] = data['publishTime'][:len('2019-11-30')]
                data_info['网址'] = 'https://www.tuniu.com/trips/%d' % data['id']
                if '2017' in data['publishTime']:
                    json_path = '../2017/途牛/%s/%s.json' % (city, city)

                if '2018' in data['publishTime']:
                    json_path = '../2018/途牛/%s/%s.json' % (city, city)
                # with open(json_path, 'r', encoding='utf-8') as f1:
                #     data_list = json.load(f1)
                # data_list.append(data_info)
                # with open(json_path, 'w', encoding='utf-8') as f1:
                #     f1.write(json.dumps(data_list))
                await Common.task_queue.put((data_info,json_path))



async def monitor_finish():
    while len(asyncio.Task.all_tasks()) > 3:
        await asyncio.sleep(1)
    await asyncio.sleep(5)
    raise SystemExit()

async def main():
    for year in ('2017', '2018'):
        for city in ('神农架', '潜江', '天门', '仙桃'):
            start_url = 'https://trips.tuniu.com/travels/index/ajax-list?queryKey=%s' % city
            await Common.start_url_queue.put((start_url,city))


                # if data['src_url']:
                #     for src_num, src in enumerate(data['src_url']):
                #         src_name = '%d-%s-图片%d' % (data_num+1, headline, src_num+1)
                #         src_name = re.sub(r'[|:?<>\\/\u3000]','', src_name)
                #         if not os.path.exists(file_path + '/images'):
                #             os.makedirs(file_path + '/images')
                #         src_path = file_path + '/images/' + '%s.jpg' % src_name
                #         flag = 'procession --> %s--%s--%sS' % (date_time, city, src_name)
                #         await Common.picture_task_queue.put((src,src_path,flag))
    for _ in range(6):
        loop.create_task(get_api_link(Common.start_url_queue))

    # for _ in range(20):
    #     loop.create_task(fetch(Common.picture_task_queue))
    #     await asyncio.sleep(1)
    await asyncio.sleep(2)

    for _ in range(6):
        loop.create_task(filter_and_get_url(Common.page_queue))

    await asyncio.sleep(2)
    for _ in range(6):
        loop.create_task(get_and_parse(Common.task_queue))
        await asyncio.sleep(1)
    loop.create_task(monitor_finish())




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()