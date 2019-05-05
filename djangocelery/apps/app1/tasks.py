from __future__ import absolute_import, unicode_literals
from djangocelery.celery import app

#
# @app.task
# def add(x,y):
#
#     sum = x + y
#     # print(sum)
#     return x + y

from time import sleep


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
from celery import Task
class demotask(Task):


@app.task
def add(x,y):
    return x + y


