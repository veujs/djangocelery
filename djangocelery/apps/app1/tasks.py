from __future__ import absolute_import, unicode_literals
from djangocelery.celery import app

import logging
logger = logging.getLogger('views_error')





# from time import sleep


# @app.task
# def Task_A(message):
#     Task_A.update_state(state='PROGRESS', meta={'progress': 0})
#     sleep(10)
#     Task_A.update_state(state='PROGRESS', meta={'progress': 30})
#     sleep(10)
#     return message
#
#
# def get_task_status(task_id):
#     task = Task_A.AsyncResult(task_id)
#
#     status = task.state
#     progress = 0
#
#     if status == u'SUCCESS':
#         progress = 100
#     elif status == u'FAILURE':
#         progress = 0
#     elif status == 'PROGRESS':
#         progress = task.info['progress']
#
#     return {'status': status, 'progress': progress}
# 使用内部的钩子函数，对函数进行重写，实现自己需要的功能
# from celery import Task
# class demotask(Task):
from time import sleep
import random
i = 0
m = 0
from celery.exceptions import SoftTimeLimitExceeded
# @app.task(time_limit=8)
# soft_time_limit  用于设置软时间设置，当任务执行时间超过这个时间，就会报错
# time_limit=10
@app.task(soft_time_limit=10)
def add(x,y):
    # try:
    # logger.info("shenmdongxi")
    # logger.error("asdfasdfsadfsadfsadfsadfasdfwadf")
    global i
    global m
    m += 10
    j = random.randint(6,9)
    print("this is a task test ---- start")
    sleep(j)
    print("this is a task test ---- end")
    i += 1
    print('i={},j={}'.format(i,j))

    print(m)
    return x + y
    # except SoftTimeLimitExceeded:
    #     print(SoftTimeLimitExceeded)

@app.task
def add1(x,y):
    global m
    print("add1:",m)
    # logger.error("add1add1add1add1add1add1add1add1")
    return x + y


# from subprocess import call
def restart_pm2():

    from time import strftime, localtime
    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), end='')
    print(": 执行了restart_pm2函数")

    # from subprocess import call
    # print(":  1小时任务没有更新，重启pm2中....")
    #t = call(['pm2', 'start', 'all'])
    #print(t)



