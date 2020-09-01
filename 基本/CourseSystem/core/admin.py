"""
管理员视图层
"""
from interface import admin_interface, common_interface
from lib import common


admin_info = {
    'user':None
}

def admin_register():
    while True:
        username = input('请输入用户名：').strip()
        password = input('请输入密码：').strip()
        confirm_password = input('请确认密码：').strip()

        # 小的逻辑判断
        if password != confirm_password:
            print('两次输入密码不一致，请重新输入！')
            continue

        # 调用接口层，管理员注册接口
        flag, msg = admin_interface.admin_register_interface(
            username, password
        )

        if flag:
            print(msg)
            break
        else:
            print(msg)


def admin_login():
    while True:
        user = input("请输入用户名:").strip()
        pwd = input("请输入密码:").strip()

        # 调用登录接口
        flag, msg = common_interface.login_interface(
            user, pwd, "admin"
        )

        if flag:
            print(msg)
            admin_info['user'] = user
            break
        else:
            print(msg)


@common.auth('admin')
def creat_school():
    while True:
        school_name = input('请输入校区名：').strip()
        school_addr = input('请输入校区地址：').strip()

        # 调用创建学校接口
        flag, msg = admin_interface.admin_creat_school_interface(
            school_name, school_addr, admin_info.get('user')
        )

        if flag:
            print(msg)
            break
        else:
            print(msg)

@common.auth('admin')
def creat_course():
    while True:
        # 打印可以选择的校区
        flag, msg = common_interface.get_all_school_interface()
        if not flag:
            print(msg)
            break

        for index, school in enumerate(msg):
            print(f'编号：{index}      校区：{school}')

        # 选择校区
        choice = input('请输入校区编号：').strip()

        try:
            choice = int(choice)
        except ValueError:
            print('输入有误请重新输入！')
            continue

        if choice not in range(len(msg)):
            print(f'编号：{choice}, 不在范围内！')
            continue

        course_name = input('创建课程名：').strip()
        course_price = input('设定课程价格：').strip()

        # 调用创建班级的接口
        flag, msg = admin_interface.admin_creat_course_interface(
            course_name, course_price, msg[choice], admin_info.get('user')
        )

        if flag:
            print(msg)
            break
        else:
            print(msg)


@common.auth('admin')
def creat_teacher():
    while True:
        teacher_name = input('请输入创建的讲师用户名：').strip()

        # 调用interface 的 admin_creat_teacher()接口
        flag, msg = admin_interface.admin_creat_teacher_interface(
            teacher_name, admin_info.get('user')
        )

        if flag:
            print(msg)
            break
        else:
            print(msg)


func_dict = {
    '1': admin_register,
    '2': admin_login,
    '3': creat_school,
    '4': creat_course,
    '5': creat_teacher,
}

def admin_view():
    while True:
        print(
            '''
            ====== 管理员界面 ======

                   1.注册
                   2.登录
                   3.创建学校
                   4.创建课程
                   5.创建讲师

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
