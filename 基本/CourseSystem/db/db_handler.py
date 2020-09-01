'''
数据处理层
'''
import pickle, os

from conf import settings


def save(obj):

    # 1.获取类名
    class_name = obj.__class__.__name__

    # 2。判断文件目录是否存在，若不存在创建文件路径·
    file_dir = os.path.join(settings.DB_PATH, class_name)
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)

    # 3.保存对象到文件, 通过pickle
    file_path = os.path.join(
        file_dir, obj.user
    )
    with open(file_path, 'wb') as f1:
        pickle.dump(obj,f1,)


def select_data(cls, user):

    # 又cls类获取类名
    class_name = cls.__name__
    file_path = os.path.join(
        settings.DB_PATH, class_name, user
    )

    # 2.判断文件是否存在
    # 2.1）文件存在，返回对象
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f1:
            obj = pickle.load(f1)
            return obj

    # 2.2) 若不存在,返回None