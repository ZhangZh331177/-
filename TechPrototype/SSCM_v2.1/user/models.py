# usr/bin/env python3
# -*- coding:utf-8- -*-
from django.db import models
from django.core.exceptions import ValidationError

# 定义验证器
def validate_pas_length(value):
    if len(value) < 6 or len(value) > 12:
        raise ValidationError('密码的长度应为6~12个字符')
def validate_stu_length(value):
    if len(value) != 12:
        raise ValidationError('学号的长度应为12')
def validate_length(value):
    if len(value) != 12:
        raise ValidationError('教职工号的长度应为12')
    
class Student(models.Model):
    genders = [
        ("m", "男"),
        ("f", "女")
    ]
    grades = [
        (1, 2017),
        (2, 2018),
        (3, 2019),
        (4, 2020),
        (5, 2021),
        (6, 2022),
        (7, 2023),
        (8, 2024)
    ]

    name = models.CharField(max_length=50, verbose_name="姓名")
    gender = models.CharField(max_length=10, choices=genders, default='m', verbose_name="性别")
    # birthday = models.DateField(verbose_name="生日")
    grade = models.IntegerField(choices=grades, default=1, verbose_name="入学年份")
    number = models.CharField(max_length=30, verbose_name="学号", primary_key=True, validators=[validate_stu_length])
    email = models.EmailField(max_length=254, verbose_name="邮箱")
    password = models.CharField(max_length=30, verbose_name="密码", validators=[validate_pas_length])
    # info = models.CharField(max_length=255, verbose_name="个人简介", null=True, default='无', help_text="自我介绍，不超过250字")
    """
    class Meta:
        constraints = [
            # 复合主键：保证 grade和number组合的student_id唯一
            models.UniqueConstraint(fields=['grade', 'number'], name='student_id'),
        ]
    """
    def get_id(self):
        return self.number
    
    def __str__(self):
        return "%s (%s)" % (self.number, self.name)


class Teacher(models.Model):
    genders = [
        ("m", "男"),
        ("f", "女")
    ]
    """
    name = models.CharField(max_length=50, verbose_name="姓名")
    gender = models.CharField(max_length=10, choices=genders, default='m', verbose_name="性别")
    birthday = models.DateField(verbose_name="生日")
    email = models.EmailField(verbose_name="邮箱")
    info = models.CharField(max_length=255, verbose_name="教师简介", help_text="不要超过250字")

    department_no = models.CharField(max_length=3, verbose_name="院系号")
    number = models.CharField(max_length=7, verbose_name="院内编号")
    password = models.CharField(max_length=30, verbose_name="密码")

    class Meta:
        constraints = [
            # 复合主键：保证 department_no 和number组合的 teacher_id 唯一
            models.UniqueConstraint(fields=['department_no', 'number'], name='teacher_id'),
        ]
    """
    name = models.CharField(max_length=50, verbose_name="姓名")
    gender = models.CharField(max_length=10, choices=genders, default='m', verbose_name="性别")
    number = models.CharField(max_length=30, verbose_name="教职工号", primary_key=True, validators=[validate_length])
    email = models.EmailField(max_length=254,verbose_name="邮箱")
    password = models.CharField(max_length=30, verbose_name="密码", validators=[validate_pas_length])
    # info = models.CharField(max_length=255, verbose_name="个人简介", null=True, default='无', help_text="自我介绍，不超过250字")

class Manager(models.Model):
    genders = [
        ("m", "男"),
        ("f", "女")
    ]
    name = models.CharField(max_length=50, verbose_name="姓名")
    gender = models.CharField(max_length=10, choices=genders, default='m', verbose_name="性别")
    number = models.CharField(max_length=30, verbose_name="教职工号", primary_key=True, validators=[validate_length])
    email = models.EmailField(max_length=254,verbose_name="邮箱")
    password = models.CharField(max_length=30, verbose_name="密码", validators=[validate_pas_length])
    # info = models.CharField(max_length=255, verbose_name="个人简介", null=True, default='无', help_text="自我介绍，不超过250字")


