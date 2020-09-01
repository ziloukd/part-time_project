import json
import os

CITY_LIST = ['武汉', '宜昌', '黄石', '十堰', '襄阳', '鄂州', '荆州', '荆门', '黄冈', '咸宁', '孝感', '随州', '恩施', '神农架','潜江', '天门', '仙桃']
for year in ('2017', '2018'):
    for city in CITY_LIST:
        file_name = '%s_new.json' % city
        file_path = os.path.join('../%s/携程'%year, city)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(os.path.join(file_path,file_name), 'w', encoding='utf-8') as f1:
            f1.write(json.dumps([]))
slice