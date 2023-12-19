# usr/bin/env python3
# -*- coding:utf-8- -*-
import random

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect

from constants import INVALID_KIND
from user.forms import StuLoginForm, TeaLoginForm, ManLoginForm
from user.models import Student, Teacher, Manager

from user.cbvs import CreateStudentView, CreateTeacherView, CreateManagerView
from user.cbvs import UpdateStudentView, UpdateTeacherView, UpdateManagerView


def home(request):
    return render(request, "user/login_home.html")


# def login(request, kind)
def login(request, *args, **kwargs):
    if not kwargs or "kind" not in kwargs or kwargs["kind"] not in ["teacher", "student", "manager"]:
        return HttpResponse(INVALID_KIND)
    kind = kwargs["kind"]
    if request.method == 'POST':
        if kind == "teacher":
            form = TeaLoginForm(data=request.POST)
        elif kind == "manager":
            form = ManLoginForm(data=request.POST)
        else:
            form = StuLoginForm(data=request.POST)
        if form.is_valid():
            uid = form.cleaned_data["uid"]
            if False:# 这里留一个窗口如果限定条件例如账户长度，可返回报错
                form.add_error("")
            else:
                if kind == "teacher":
                    # department_no = uid[:3]
                    # number = uid[3:]
                    object_set = Teacher.objects.filter(number=uid)
                elif kind == "manager":
                    object_set = Manager.objects.filter(number=uid)
                else:
                    # grade = uid[:4]
                    # number = uid[4:]
                    object_set = Student.objects.filter(number=uid)
                if object_set.count() == 0:
                    form.add_error("uid", "该账号不存在.")
                else:
                    user = object_set[0]
                    if form.cleaned_data["password"] != user.password:
                        form.add_error("password", "密码不正确.")
                    else:
                        request.session['kind'] = kind
                        request.session['user'] = uid
                        request.session['id'] = uid # user.id
                        # successful login
                        to_url = reverse("course", kwargs={'kind': kind})
                        return redirect(to_url)
            return render(request, 'user/login_detail.html', {'form': form, 'kind': kind})
    else:
        context = {'kind': kind}
        if request.GET.get('uid'):
            uid = request.GET.get('uid')
            context['uid'] = uid
            if kind == "teacher":
                form = TeaLoginForm({"uid": uid, 'password': '12345678'})
            elif kind == "manager":
                form = ManLoginForm({"uid": uid, 'password': '12345678'})
            else:
                form = StuLoginForm({"uid": uid, 'password': '12345678'})
        else:
            if kind == "teacher":
                form = TeaLoginForm()
            elif kind == "manager":
                form = ManLoginForm()
            else:
                form = StuLoginForm()
        context['form'] = form
        if request.GET.get('from_url'):
            context['from_url'] = request.GET.get('from_url')
        return render(request, 'user/login_detail.html', context)


def logout(request):
    if request.session.get("kind", ""):
        del request.session["kind"]
    if request.session.get("user", ""):
        del request.session["user"]
    if request.session.get("id", ""):
        del request.session["id"]
    return redirect(reverse("login"))


def register(request, kind):
    func = None
    if kind == "teacher":
        func = CreateTeacherView.as_view()
    elif kind == "manager":
        func = CreateManagerView.as_view()
    else:
        func = CreateStudentView.as_view()
    if func:
        return func(request)
    else:
        return HttpResponse(INVALID_KIND)


def update(request, kind):
    func = None
    if kind == "teacher":
        func = UpdateTeacherView.as_view()
    elif kind == "manager":
        func = UpdateManagerView.as_view()
    else:
        func = UpdateStudentView.as_view()
    if func:
        pk = request.session.get("id", "")
        if pk:
            context = {
                "name": request.session.get("name", ""),
                "kind": request.session.get("kind", ""),
            }
            return func(request, pk=pk, context=context)
        else:
            return redirect(reverse("login"))
    else:
        return HttpResponse(INVALID_KIND)



