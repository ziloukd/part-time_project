import asyncio
import aiohttp
import re
import os
import json
from lxml import etree
import time
from asyncio.queues import Queue


class Common():
    id_queue = Queue()
    request_queue = Queue()
    picture_queue = Queue()
    request_and_parse_queue = Queue()
    CITY_LIST = ['武汉','宜昌','黄石','十堰','襄阳','鄂州','荆州','荆门','黄冈','咸宁','孝感','随州','恩施','神农架','潜江', '天门', '仙桃']
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}


async def get_session(url,type, *args):
    async with aiohttp.ClientSession() as session:
        """发起请求，根据不同的需求，返回text或文本"""
        try:
            response = await session.get(url, headers=Common.headers, timeout=10)
        except asyncio.exceptions.TimeoutError as e:
            return '超时' , 404
        if type == 'html':
            return await response.text(),response.status
        if type == 'json':
            return await response.json(), response.status
        if type == 'content':
            return await response.read(), response.status

async def get_id_and_make_apilink(queue):
    end_flags = True
    while end_flags:
        try:
            url, city = queue.get_nowait()
        except:
            end_flags = False
            continue
        await asyncio.sleep(1)
        response,status = await asyncio.create_task(get_session(url, 'html'))

        tree = etree.HTML(response)

        # 襄阳和神龙架是个例外
        if city == '襄阳':
            id_url = '300121'
        elif city == '神农架':
            id_url = '299062'

        else:

            id_url = tree.xpath("//*[contains(text(),'查看全部相关攻略')]/@href")[0]

        city_num = re.findall('\d{5,}' ,id_url)[0]
        print(city_num, city)
        cnt = 0
        # 获取cnt_max临界值（循环终止条件）
        api_link = 'https://touch.go.qunar.com/api/proxy/book/search?type=2&distIds=%s&limit=12&offset=%d' % (
        city_num, 0)
        json_response,status = await asyncio.create_task(get_session(api_link, 'json'))
        cnt_max = json_response['data']['totalCount']

        while 1:
            api_link = 'https://touch.go.qunar.com/api/proxy/book/search?type=2&distIds=%s&limit=12&offset=%d' % (city_num, cnt)
            await Common.request_queue.put((api_link, city))
            cnt += 1
            if cnt >= cnt_max:
                break


async def filter_and_save(queue):
    # 筛选符合抓取条件的数据
    end_flags = True
    while end_flags:
        try:
            url, city = queue.get_nowait()
        except:
            end_flags = False
            continue

        json_response, status = await asyncio.create_task(get_session(url, 'json'))
        #
        for retry_time in range(3):
            if status == 200:
                break
            else:
                await asyncio.sleep(0.2)
                json_response, status = await asyncio.create_task(get_session(url, 'json'))

        # 保存的数据结构
        data_info = {
            '来源':'去哪儿',
            '城市':city,
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

        # 获取初步筛选时间在2017-2018的数据
        for data in json_response['data']['list']:
            date_time = data['startTime']
            if 1483200000000 <= date_time < 1546272000000:
                # 时间戳转日期
                timeStamp = date_time / 1000
                timeArray = time.localtime(timeStamp)
                otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
                data_info['发表时间'] = otherStyleTime
                # print(city,otherStyleTime)
                # 网址
                data_info['网址'] = f'https://travel.qunar.com/travelbook/note/{data["id"]}'
                data_info['标题'] = data['title']
                # 文件名和保存路径
                file_name = '%s.json' % city
                if re.findall('2017', otherStyleTime):
                    file_catalog = '../2017/去哪儿/%s' % city
                elif re.findall('2018', otherStyleTime):
                    file_catalog = '../2018/去哪儿/%s' % city
                else:
                    continue
                if not os.path.exists(file_catalog):
                    os.makedirs(file_catalog)
                file_path = os.path.join(file_catalog, file_name)

                with open(file_path, 'r', encoding='utf-8') as f1:
                    data_list = json.load(f1)
                data_list.append(data_info)
                # 去重
                data_list = [dict(t) for t in set([tuple(d.items()) for d in data_list])]
                with open(file_path, 'w', encoding='utf-8') as f1:
                    f1.write(json.dumps(data_list))
                print(city, data_info)


async def detail_parse(queue):
    end_flag = True
    while end_flag:
        try:
            data_dic = queue.get_nowait()
            # print(data_dic)
        except:
            end_flag = False
            continue

        response,status = await asyncio.create_task(get_session(data_dic['网址'], 'html'))
        for retry_time in range(3):
            if status == 200:
                break
            else:
                await asyncio.sleep(0.2)
                response, status = await asyncio.create_task(get_session(data_dic['网址'], 'html'))

        # 解析网页完善数据
        # 锁定抓取内容的大致位置
        ret = re.compile('<!-- 行程安排.*?-->(.*?)<!-- 行程安排.*?-->', re.S)
        html = ret.findall(response)[0]
        tree = etree.HTML(html)
        try:
            data_dic['游玩时间'] = tree.xpath("//p[contains(text(), '出发日期')]/span[2]/text()")[0]
        except:
            pass
        try:
            data_dic['天数'] = tree.xpath("//p[contains(text(), '天数')]/span[2]/text()")[0]
        except:
            pass
        try:
            play_list = tree.xpath("//p[contains(text(), '玩法')]/span/span/text()")
            data_dic['玩法'] = ','.join([i.strip() for i in play_list])
        except:
            pass
        try:
            data_dic['人均花费'] = tree.xpath("//p[contains(text(), '人均费用')]/span/span/text()")[0]
        except:
            pass
        try:
             people_list = tree.xpath("//p[contains(text(), '人物')]/span/span/text()")
             data_dic['和谁'] = ','.join([i.strip() for i in people_list])
        except:
            pass
        try:
             people_list = tree.xpath("//p[contains(text(), '人物')]/span/span/text()")
             data_dic['和谁'] = ','.join([i.strip() for i in people_list])
        except:
            pass
        try:
             content_list = tree.xpath("//div[@id='b_panel_schedule']//text()")
             content = re.sub(r'\+1','',''.join([i.strip() for i in content_list]))
             data_dic['正文'] = content
        except:
            pass
        ret = re.compile('<!-- 最新评论.*?-->(.*?)<!-- 最新评论.*?-->', re.S)
        html = ret.findall(response)[0]
        comment_tree = etree.HTML(html)
        try:
             comment_list = comment_tree.xpath("//dl/dd/div/text()")
             comment = '\n'.join([str(index+1) + '.' + i.strip() for index,i in enumerate(comment_list)])
             data_dic['评论'] = comment
        except:
            pass
        queue.task_done()


async def download_picture(queue):
    end_flag = True
    while end_flag:
        try:
            src, path = queue.get_nowait()
        except:
            end_flag = False
            continue
        try:
            content_response, status = await asyncio.create_task(get_session(src, 'content'))
        except:
            pass
        #
        for retry_time in range(3):
            if status == 200:
                break
            else:
                await asyncio.sleep(0.2)
                content_response, status = await asyncio.create_task(get_session(src, 'json'))

        # 图片保存
        print(path)
        with open(path, 'wb') as f1:
            f1.write(content_response)

async def monitor_finish():
    while len(asyncio.Task.all_tasks()) > 3:
        await asyncio.sleep(1)
    await asyncio.sleep(5)
    raise SystemExit()

async def main():
        # for city in Common.CITY_LIST:
        #     start_url = 'https://travel.qunar.com/search/all/%s' % city
        #     await Common.id_queue.put((start_url, city))


        for year in ('2017', '2018'):
            for city in Common.CITY_LIST:
                if city in ('武汉','宜昌','黄石',):
                    continue
                with open('../%s/去哪儿/%s/%s_new.json' % (year, city,city) , encoding='utf-8') as f1:
                    li = json.load(f1)
                # 创建图片保存目录
                file_catalog = '../%s/去哪儿/%s/images' % (year, city)
                if not os.path.exists(file_catalog):
                    os.makedirs(file_catalog)
                # 去重，排序
                temp_list = list(set([str(i) for i in li]))
                li = [eval(i) for i in temp_list]
                data_list = sorted(li, key=lambda d: (d['发表时间'],d['标题']))
                if not data_list:
                    continue
                for data_num,data in enumerate(data_list):
                    if year == '2017' and city == '武汉':
                        if data_num < 122:
                            continue
                    # else:
                    #     continue
                    src_list = data['src_url']
                    headline = data['标题']
                    if not src_list:
                        continue
                    for src_num, src in enumerate(src_list):
                        src_name = re.sub(r'["|:?<>\\/\u3000\s]', '', f'{data_num+1}-{headline}-图片{src_num+1}.jpg')
                        path = os.path.join(file_catalog, src_name)
                        await Common.picture_queue.put((src, path))

        # 图片下载
        for _ in range(30):
            loop.create_task(download_picture(Common.picture_queue))
        # 起始页
        # for _ in range(3):
        #     loop.create_task(get_id_and_make_apilink(Common.id_queue))
        # #
        # await asyncio.sleep(15)
        # #
        # print(Common.request_queue.qsize())
        # for _ in range(3):
        #     loop.create_task(filter_and_save(Common.request_queue))


        # await asyncio.sleep(15)
        # print(Common.request_and_parse_queue.qsize())
        # for _ in range(2):
        #     loop.create_task(detail_parse(Common.request_and_parse_queue))
        #     await asyncio.sleep(2)

        loop.create_task(monitor_finish())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

