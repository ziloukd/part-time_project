"""
学生视图层
"""
from interface import student_interface, common_interface
from lib import common


student_info = {
    'user':None
}


def student_register():
    while True:
        user = input('请输入用户名：').strip()
        pwd = input('请输入密码：').strip()
        confirm_pwd = input('请确认密码：').strip()

        # 验证确认密码是否和密码一致
        if pwd != confirm_pwd:
            print('两次密码不一致，请确认密码是否正确！')
            continue

        # 调用注册接口
        flag, msg = student_interface.register_interface(
            user, pwd
        )

        if flag:
            print(msg)
            break
        else:
            print(msg)


def student_login():
    while True:
        user = input("请输入用户名:").strip()
        pwd = input("请输入密码:").strip()

        # 调用登录接口
        flag, msg = common_interface.login_interface(
            user, pwd, "student"
        )

        if flag:
            print(msg)
            student_info['user'] = user
            break
        else:
            print(msg)



@common.auth('student')
def choose_school():
    while True:
        # 调用公共接口的显示所有学校功能，获取校区列表
        flag, school_list = common_interface.get_all_school_interface()


        if not school_list:
            print(school_list)
        # 打印校区列表
        for index, school in enumerate(school_list):
            print(f'编号：[{index}]        校区：{school}')

        #
        choice = input('请输入校区编号：').strip()

        try:
            choice = int(choice)
        except ValueError:
            print('输入有误！')

        if choice not in range(len(school_list)):
            print(f'编号:[{choice}]，不在范围内。')

        print(school_list[choice])
        # 调用选择校区接口
        flag, msg = student_interface.choose_school(
            school_list[choice], student_info.get('user')
        )

        if flag:
            print(msg)
            break
        else:
            print(msg)


@common.auth('student')
def choose_course():
    while True:
        # 调用显示所有课程的接口
        flag, msg = common_interface.get_course(
            student_info.get('user')
        )

        if not flag:
            print(msg)
            continue

        # 打印可选课程
        for index, course in enumerate(msg):
            print(f'编号：[{index}]      课程：{course.user}')

        #
        choice = input('请输入课程编号：').strip()

        try:
            choice = int(choice)
        except ValueError:
            print('输入有误！')

        if choice not in range(len(msg)):
            print(f'编号:[{choice}]，不在范围内。')

        # 调用选择课程接口
        flag, msg = student_interface.choose_course(
            msg[choice].user, student_info.get('user')
        )

        if flag:
            print(msg)
            break
        else:
            print(msg)


@common.auth('student')
def check_score():
    # 调用查看分数接口：
    flag, msg = student_interface.check_score(
        student_info.get('user')
    )
    print(msg)
    for index,course in enumerate(msg):
        print(course)
        print(f'编号:[{index}]    课程：{course}')




func_dict = {
    '1': student_register,
    '2': student_login,
    '3': choose_school,
    '4': choose_course,
    '5': check_score,
}

def student_view():
    while True:
        print(
            '''
            ====== 学生界面 ======

                   1.注册
                   2.登录
                   3.选择校区
                   4.选择课程
                   5.查看分数

            ======== end ========       
            '''
        )
        user_choice = input('请输入选择的功能编号：').strip()

        if user_choice == 'q':
            break

        if user_choice not in func_dict:
            print('输入有误！')
            continue

        func_dict.get(user_choice)()