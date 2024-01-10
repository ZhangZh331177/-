# usr/bin/env python
# -*- coding:utf-8- -*-
from django import forms
from .models import Course, Schedule, StudentCourse
from user.models import Teacher
from django.core.exceptions import ValidationError

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        exclude = ['status']
        # fields = ['teacher']
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].choices = Teacher.get_teacher_list()

    def clean_max_number(self):
        max_number = self.cleaned_data.get('max_number')
        if max_number is not None:
            if max_number <= 0:
                raise ValidationError('最大人数必须大于0')
        return max_number

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        exclude = ["course"]
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        start_week = cleaned_data.get("start_week")
        end_week = cleaned_data.get("end_week")
        if start_time is not None and end_time is not None:
            if start_time > end_time:
                raise ValidationError("开始时间必须小于结束时间")
            if start_week > end_week:
                raise ValidationError("开始周数必须小于结束周数")
        return cleaned_data


class ScoreForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = ["student", "course", "scores", "comments"]

    student = forms.CharField(label="学生", disabled=True)
    # course = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    course = forms.CharField(label="课程", disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['student'] = self.instance.student
        self.initial['course'] = self.instance.course

    def clean_student(self):
        return self.initial['student']

    def clean_course(self):
        return self.initial['course']


class RateForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = ["course", "rating", "assessment"]

    course = forms.CharField(label="课程", disabled=True)
    # scores = forms.IntegerField(label="成绩", disabled=True)
    # comments = forms.CharField(label="老师评价", disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['course'] = self.instance.course
        # self.initial['scores'] = self.instance.scores
        # self.initial['comments'] = self.instance.comments

    def clean_course(self):
        return self.initial['course']

    def clean_scores(self):
        return self.initial['scores']

    def clean_comments(self):
        return self.initial['comments']
