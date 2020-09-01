"""
教师视图层
"""
from interface import teacher_interface, common_interface
from lib import common


teacher_info = {
    'user':None
}


def teacher_login():
    while True:
        user = input("请输入用户名:").strip()
        pwd = input("请输入密码:").strip()

        # 调用登录接口
        flag, msg = common_interface.login_interface(
            user, pwd, "teacher "
        )

        if flag:
            print(msg)
            break
        else:
            print(msg)


@common.auth('teacher')
def check_course():
    pass


@common.auth('teacher')
def chose_course():
    pass


@common.auth('teacher')
def check_student():
    pass


@common.auth('teacher')
def modify_sore():
    pass


func_dict = {
    '1': teacher_login,
    '2': check_course,
    '3': chose_course,
    '4': check_student,
    '5': modify_sore,
}

def teacher_view():
    while True:
        print(
            '''
            ====== 教师界面 ======

                   1.登录
                   2.查看教授课程
                   3.选择教授课程
                   4.查看课程下的学生
                   5.修改学生分数

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