from django.db import models
import datetime
from user.models import Student, Teacher
from constants import COURSE_STATUS, COURSE_OPERATION
from django.core.exceptions import ValidationError

def current_year():
    # refer: https://stackoverflow.com/questions/49051017/year-field-in-django/49051348
    return datetime.date.today().year

class Course(models.Model):
    credits = [
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)
    ]
    semesters = [
        ("Autumn", "春"), ("Spring", "秋")
    ]
    name = models.CharField(max_length=50, verbose_name="课程名")# , unique=True)
    introduction = models.CharField(max_length=250, verbose_name="介绍")
    credit = models.IntegerField(choices=credits, verbose_name="学分")
    max_number = models.IntegerField(verbose_name="课程最大人数")

    year = models.IntegerField(verbose_name="年份", default=current_year)
    semester = models.CharField(max_length=20, verbose_name="学期", choices=semesters)

    # COURSE_STATUS
    # 1: "未开始选课",
    # 2: "开始选课",
    # 3: "结束选课",
    # 4: "学生评教中",
    # 5: "评教已结束",
    # 6: "教师给分中",
    # 7: "已结课"

    status = models.IntegerField(verbose_name="课程状态", default=1)

    teacher = models.ForeignKey(Teacher, verbose_name="课程教师", on_delete=models.CASCADE)

    def get_status_text(self):
        return COURSE_STATUS[self.status]

    def get_op_text(self):
        return COURSE_OPERATION[self.status]

    def get_current_count(self):
        courses = StudentCourse.objects.filter(course=self, with_draw=False)
        return len(courses)

    def get_schedules(self):
        schedules = Schedule.objects.filter(course=self)
        return schedules

    def __str__(self):
        return "%s (%s)" % (self.name, self.teacher.name)


class Schedule(models.Model):
    weekdays = [(1, "周一"), (2, "周二"), (3, "周三"), (4, "周四"), (5, "周五"), (6, "周六"), (7, "周日")]
    
    weekday = models.IntegerField(choices=weekdays, verbose_name="日期")



    classes = [(1,"第一节"),(2,"第二节"),(3,"第三节"),(4,"第四节"),(5,"第五节"),(6,"第六节"),(7,"第七节"),(8,"第八节"),]
    
    start_time = models.IntegerField(verbose_name="开始时间", choices = classes, default=1)
    end_time = models.IntegerField(verbose_name="结束时间", choices = classes, default=1)
    location = models.CharField(max_length=100, verbose_name="上课地点")
    remarks = models.CharField(max_length=100, verbose_name="备注", null=True, blank = True)

    weeks = [(1,"第一周"),(2,"第二周"),(3,"第三周"),(4,"第四周"),(5,"第五周"),(6,"第六周"),(7,"第七周"),(8,"第八周"),]
    start_week = models.IntegerField(verbose_name="开始周", choices = weeks, default = 1)
    end_week = models.IntegerField(verbose_name="结束周", choices = weeks, default = 1)

    intervals = [(1, "无间隔"), (2, "每隔一周上一次")]
    week_interval = models.IntegerField(verbose_name="周间隔", choices=intervals, default=1)

    course = models.ForeignKey(Course, verbose_name="课程名", on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = ('field1', 'field2')

    def __str__(self):
        s = "第%s周-第%s周 " % (self.start_week, self.end_week)
        if self.week_interval == 2:
            s += "隔一周 "
        s += "%s 第%s节-第%s节 " % (self.get_weekday_display(), self.start_time,
                            self.end_time)
        s += "在%s" % self.location
        if self.remarks:
            s += " %s" % self.remarks
        return s


class StudentCourse(models.Model):
    create_time = models.DateTimeField(auto_now=True)
    with_draw = models.BooleanField(default=False)
    with_draw_time = models.DateTimeField(default=None, null=True)

    scores = models.IntegerField(verbose_name="成绩", null=True)
    comments = models.CharField(max_length=250, verbose_name="老师评价", null=True)

    rates = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]

    rating = models.IntegerField(verbose_name="学生评分", choices=rates, null=True, help_text="5分为最满意，最低分是1分")
    assessment = models.CharField(max_length=250, verbose_name="学生评价", null=True)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
