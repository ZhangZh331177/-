# usr/bin/env python
# -*- coding:utf-8- -*-
from django import forms
from .models import Student, Teacher, Manager


class StuLoginForm(forms.Form):
    uid = forms.IntegerField(label='学号',max_value=1e20)
    password = forms.CharField(label='密码', max_length=30, widget=forms.PasswordInput)

class TeaLoginForm(forms.Form):
    uid = forms.IntegerField(label='教职工号', max_value=1e10)
    password = forms.CharField(label='密码', max_length=30, widget=forms.PasswordInput)

class ManLoginForm(forms.Form):
    uid = forms.IntegerField(label='教职工号', max_value=1e10)
    password = forms.CharField(label='密码', max_length=30, widget=forms.PasswordInput)


class StuRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="确认密码")

    class Meta:
        model = Student
        fields = ('name','gender','grade',# 姓名，性别，年级，学号，邮箱，密码
                  'number','email','password','confirm_password')

    def clean(self):
        cleaned_data = super(StuRegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if confirm_password != password:
            self.add_error('confirm_password', 'Password does not match.')
        return cleaned_data

class TeaRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="确认密码")

    class Meta:
        model = Teacher
        fields = ('name','gender',# 姓名，性别，年级，学号，邮箱，密码
                  'number','email','password','confirm_password')

    def clean(self):
        cleaned_data = super(TeaRegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if confirm_password != password:
            self.add_error('confirm_password', 'Password does not match.')

class ManRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="确认密码")

    class Meta:
        model = Manager
        fields = ('name','gender',# 姓名，性别，年级，学号，邮箱，密码
                  'number','email','password','confirm_password')

    def clean(self):
        cleaned_data = super(ManRegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if confirm_password != password:
            self.add_error('confirm_password', 'Password does not match.')
"""
class StuUpdateForm(StuRegisterForm):
    class Meta:
        model = Student
        fields = ('name',
                  'password',
                  'confirm_password',
                  'gender',
                  'birthday',
                  'email',
                  'info')
"""
