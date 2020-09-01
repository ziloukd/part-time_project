from db import models
from lib import common


# 管理员注册接口
def register_interface(user, pwd):
    # 1. 判断用户是否存在
    # 调用Admin类中的，select方法
    # 由该方法调用db_handler中的select_data功能，获取对象
    student_obj = models.Student.select(user)

    # 1.1) 若用户存在,则不允许注册，返回用户已存在给视图层
    if student_obj:
        return False, '用户已存在！'

    # 1.2) 若不存在则允许注册，调用类实例化得到对象并保存
    # 存入之前，先对密码进行加密
    pwd = common.get_md5_pwd(pwd)
    student_obj = models.Student(user, pwd)
    # 对象调用save() 会将admin_obj传递给save方法
    student_obj.save()

    return True, '注册成功！'


# 选择学校
def choose_school(school, user):
    # 1.获取学生对象
    student_obj = models.Student.select(user)

    # 2.调用选择校区功能
    student_obj.choose_school(school)


    return True, '选择成功！'


# 选择课程
def choose_course(course, user):
    # 1.获取学生对象
    student_obj = models.Student.select(user)

    # 2.添加课程
    student_obj.choose_course(course)

    return True,'添加成功！'


# 查看分数
def check_score(user):
    # 获取学生对象
    student_obj = models.Student.select(user)

    # 调用查看分数功能，返回课程信息列表

    return True, student_obj.score_dict