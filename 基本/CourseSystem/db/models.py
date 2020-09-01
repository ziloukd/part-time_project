'''
抽象类
'''
from db import db_handler


class Base:
    def save(self):
        res = db_handler.save(self)

    @classmethod
    def select(cls, username):
        obj = db_handler.select_data(cls, username)
        return obj

class Admin(Base):
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd

    # 创建校区
    def creat_school(self, school_name,school_addr):
        # 1.实例化校区一个对象
        school_obj = School(school_name, school_addr)

        # 2.保存数据
        school_obj.save()

    # 创建班级
    def creat_course(self, course_name, school_obj):
        # 1.更新校区数据
        school_obj.course_list.append(course_name)
        school_obj.save()

    # 创建讲师
    def creat_teacher(self, teacher_name):
        # 1.实例化一个讲师对象
        teacher_obj = Teacher(teacher_name)

        # 2.保存数据
        teacher_obj.save()


class Student(Base):
    def __init__(self, name, pwd):
        self.user = name
        self.pwd = pwd
        self.school = None
        self.course_list = []
        self.score_dict = {}

    def choose_course(self,course):
        self.course_list.append(
            course
        )
        self.score_dict[course] = 0
        self.save()

    def choose_school(self, school):
        self.school = School.select(school)
        self.save()

    def check_score(self):
        return self.score_dict


class Teacher(Base):
    def __init__(self, name):
        self.user = name
        # 初始密码
        self.pwd = '123'

class School(Base):
    def __init__(self, name, addr):
        self.user = name
        self.addr = addr
        self.course_list = []

class Course(Base):
    def __init__(self, name, price):
        self.user = name
        self.price = price


