"""
公共接口
"""
import os
from db import models
from lib import common
from conf import settings


# 登录接口
def login_interface(user, pwd, user_type):
    # 1,判断用户类型,然后调用对应的对象
    if user_type == 'admin':
        obj = models.Admin.select(user)
    elif user_type == 'student':
        obj = models.Student.select(user)
    elif user_type == 'teacher':
        obj = models.Teacher.select(user)
    else:
        return False, '输入的角色不存在！'


    # 1.1） 若用户不存在，则不允许登录，返回用户不存在，请先注册！
    if not obj:
        return False, '用户不存在，请先注册！'

    # 1.2） 若用户存在， 判断密码是否正确
    # pwd 通过common.get_md5_pwd加密
    pwd = common.get_md5_pwd(pwd)
    if pwd == obj.pwd:
        return True, f'[{user}]登录成功！'
    else:
        return False, '密码或用户名错误！'


# 显示所有校区接口
def get_all_school_interface():
    # 1.查看School文件夹是否存在
    school_file_path = os.path.join(
        settings.DB_PATH, 'School'
    )
    # 1.1)若路径不存在，则返回False, '请先创建校区'
    if not os.path.exists(school_file_path):
        return False, '请联系管理员！'

    # 1.2）若路径存在，则获取文件夹中的所有文件列表
    # 2.获取所有文件
    school_list = os.listdir(school_file_path)

    # 2.1) 若文件列表为空则，返回False, ’请先创建校区‘
    if not school_list:
        return False, '请联系管理员！'

    # 2.2） 若文件列表不为空，则返回True, school_list
    else:
        return True, school_list


def get_course(user):
    # 查看用户选择的校区
    student_obj  = models.Student.select(user)
    school_obj = student_obj.school

    # 获取校区内所拥有的课程
    course_list = school_obj.course_list

    if not course_list:
        return False, '课程未创建，请联系管理员！'

    return True, course_list