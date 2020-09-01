"""
主用户视图层
"""
from core import admin, student, teacher

func_dict = {
    '1': admin.admin_view,
    '2': student.student_view,
    '3': teacher.teacher_view,
}


def run():
    while True:
        print(
            '''
            ====== 选课系统 ======
            
                   1.管理员
                   2.学生
                   3.教师
        
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