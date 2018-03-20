__author__ = 'shy'
__date__ = '2018/3/20 10:41'


# Create your views and use celery tasks here.
from django.shortcuts import render, HttpResponse

from proj import tasks


def task_test(request):
    res = tasks.add.delay(228, 24)
    print("start running task")
    print("async task res", res.get())

    return HttpResponse('res %s' % res.get())