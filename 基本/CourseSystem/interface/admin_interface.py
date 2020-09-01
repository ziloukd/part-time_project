'''
管理视图逻辑接口层
'''
from db import models
from lib import common


# 管理员注册接口
def admin_register_interface(user, pwd):
    # 1. 判断用户是否存在
    # 调用Admin类中的，select方法
    # 由该方法调用db_handler中的select_data功能，获取对象
    admin_obj = models.Admin.select(user)

    # 1.1) 若用户存在,则不允许注册，返回用户已存在给视图层
    if admin_obj:
        return False, '用户已存在！'

    # 1.2) 若不存在则允许注册，调用类实例化得到对象并保存
    # 存入之前，先对密码进行加密
    pwd = common.get_md5_pwd(pwd)
    admin_obj = models.Admin(user, pwd)
    # 对象调用save() 会将admin_obj传递给save方法
    admin_obj.save()

    return True, '注册成功！'


# 管理员登录接口
'''
def admin_login_interface(user, pwd):
    # 1.判断用户存不存在
    # 调用Admin类中的，select的方法
    # 该方法调用db_handler中的select_data功能获取对象
    class_name = models.Admin.__name__
    admin_obj = models.Admin.select(user)

    # 1.1） 若用户不存在，则不允许登录，返回用户不存在，请先注册！
    if not admin_obj:
        return False, '用户不存在，请先注册！'

    # 1.2） 若用户存在， 判断密码是否正确
    # pwd 通过common.get_md5_pwd加密
    pwd = common.get_md5_pwd(pwd)
    if pwd == admin_obj.pwd:
        return True, f'[{user}]登录成功！'
    else:
        return False, '密码或用户名错误！'''


# 创建校区接口
def admin_creat_school_interface(school_name, school_addr, user):
    # 1.判断校区是否存在
    # 1.1 校区已存在，则不允许创建，返回'school_name校区已创建！’
    # 调用School类的select（）功能，如果返回值非None则存在，反之则不存在
    obj = models.School.select(school_name)
    if obj:
        return False, f'[{school_name}]校区已存在！'

    # 1.2 校区不存在，则保存
    # 调用admin对象创建校区
    admin_obj = models.Admin.select(user)
    admin_obj.creat_school(school_name,school_addr)
    return True, f'[{school_name}]校区创建成功！'


def admin_creat_course_interface(course_name, course_price, school, user):
    # 1.调用school对象
    school_obj = models.School.select(school)

    # 2.判断班级是否存在
    # 2.1) 若班级存在，返回'班级已经存在'
    if course_name in school_obj.course_list:
        return False, f'[{course_name}，已存在！]'

    # 2.2）若班级不存在，则调用Admin对象创建课程
    # 创建课程对象
    course_obj = models.Course(course_name, course_price)

    admin_obj = models.Admin.select(user)
    admin_obj.creat_course(course_obj, school_obj)

    return True, f'课程:[{course_name}]创建成功！'


# 创建讲师接口
def admin_creat_teacher_interface(teacher_name, user):
    # 1.判断讲师是否存在
    teacher_obj = models.Teacher.select(teacher_name)

    # 1.1)若讲师存在，则返回，讲师{teacher_name}已存在
    if teacher_obj:
        return False, f'讲师[{teacher_name}]，已存在！'

    # 1.2) 若讲师不存在，则进入下一步
    #2. 调用管理员对象创建讲师
    admin_obj = models.Admin.select(user)
    admin_obj.creat_teacher(
        teacher_name
    )

    return True, f'讲师[{teacher_name}]，创建成功！'
