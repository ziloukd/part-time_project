import time
import re

# 时间戳转日期
timeStamp = 1389369600000/1000
timeArray = time.localtime(timeStamp)
otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
print(otherStyleTime)

# 日期转时间戳
timeArray = time.strptime('2019-1-1 00:00:00', "%Y-%m-%d %H:%M:%S")
# 轉換為時間戳:
timeStamp = int(time.mktime(timeArray))
print(timeStamp)


import os
import json
import shutil

# 建立一个模板json
CITY_LIST = ['武汉','宜昌','黄石','十堰','襄阳','鄂州','荆州','荆门','黄冈','咸宁','孝感','随州','恩施','神农架','潜江', '天门', '仙桃']
for year in ('2017', '2018'):
    for city in CITY_LIST:
        # file_name = '%s.json' % city
        # file_path = os.path.join('../%s/去哪儿'%year, city)
        # if not os.path.exists(file_path):
        #     os.makedirs(file_path)
        # with open(os.path.join(file_path,file_name), encoding='utf-8') as f1:
        #     data_list = json.load(f1)
        # for data in data_list:
        #     if '2017' in data['发表时间']:
        #         file_new_name = '%s_new.json' % city
        #         file_new_path = os.path.join('../2017/去哪儿/%s'% city, file_new_name)
        #     if '2018' in data['发表时间']:
        #         file_new_name = '%s_new.json' % city
        #         file_new_path = os.path.join('../2018/去哪儿/%s' % city, file_new_name)
        #     with open(file_new_path, encoding='utf-8') as f1:
        #         li = json.load(f1)
        #     li.append(data)
        #     with open(file_new_path, 'w', encoding='utf-8') as f1:
        #         f1.write(json.dumps(li))

        # 删除目录
        picture_path = '../%s/去哪儿/%s/images' % (year, city)
        if os.path.isdir(picture_path):
            shutil.rmtree(picture_path, True)

# # 文件名和保存路径
# file_name = '%s.json' % city
# if re.findall('2017', otherStyleTime):
#     file_catalog = '../2017/去哪儿/%s' % city
# elif re.findall('2018', otherStyleTime):
#     file_catalog = '../2018/去哪儿/%s' % city
# else:
#     continue
# if not os.path.exists(file_catalog):
#     os.makedirs(file_catalog)
# file_path = os.path.join(file_catalog, file_name)
#
# with open(os.path.join(file_path, file_name), 'r', encoding='utf-8') as f1:
#     data_list = json.load(f1)
# data_list.append(data_info)
# # 去重
# data_list = [dict(t) for t in set([tuple(d.items()) for d in data_list])]
# with open(os.path.join(file_path, file_name), 'w', encoding='utf-8') as f1:
#     f1.write(json.dumps(data_list))
# print(city, data_info)
# play_list = filter(lambda d:d if not re.findall('\s',d) else '' ,['1','  \n','4','da'])
# play = ','.join(i.strip() for i in play_list)
# print(play)

s = """
.__                 
|  |__  _  _____.__.
|  |\ \/ \/ <   |  |
|  |_\     / \___  |
|____/\/\_/  / ____|
             \/   """

print(s)

