import hashlib
import os

from conf import settings


def get_md5_pwd(pwd):
    obj = hashlib.md5()
    obj.update(pwd.encode('utf-8'))
    salt = '好好学习！'
    obj.update(salt.encode('utf-8'))
    return obj.hexdigest()


# 登录认证
def auth(role):
    from core import admin, student, teacher
    def auth_login(func):

        def inner(*args, **kwargs):
            if role == 'admin':
                if admin.admin_info.get('user'):
                    res = func(*args, **kwargs)
                    return res
                else:
                    print('请先登录！')
                    admin.admin_login()
            elif role == 'student':
                if student.student_info.get('user'):
                    res = func(*args, **kwargs)
                    return res
                else:
                    print('请先登录！')
                    student.student_login()
            elif role == 'teacher':
                if teacher.teacher_info.get('user'):
                    res = func(*args, **kwargs)
                    return res
                else:
                    print('请先登录！')
                    teacher.teacher_login()
            else:
                print('当前视图没有权限')
        return inner
    return auth_login


