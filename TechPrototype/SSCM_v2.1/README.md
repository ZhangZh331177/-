Organization

main
-user
--models.py
    设置用户模型：
    学生：姓名，性别，年级，学号，邮箱，密码，自我介绍
    教师：姓名，性别，编号，邮箱，密码，自我介绍
    管理员：姓名，性别，编号，邮箱，密码，自我介绍
--views.py
    前端
--form.py
    登录信息表单
--cbvs.py
    视图



-templates
--user
---background.html
    主界面
---login_home.html
    选择登录方式：学生/教师/管理员
---login_detail.html
---register.html
    注册界面
    
-course



```python
COURSE_STATUS = {
    1: "未开始选课",
    2: "开始选课",
    3: "结束选课",
    4: "结课",
    5: "打分完成",
}

COURSE_OPERATION = {
    1: "开始选课",
    2: "结束选课",
    3: "结课",
    4: "给分",
    5: "查看详情"
}
```