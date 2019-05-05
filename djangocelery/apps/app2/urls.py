# from django.contrib import admin
# from django.urls import path
from django.conf.urls import url, include
from apps.app2 import views

urlpatterns = [
    url(r'^v1/index_app2/$', views.index_app2),
    # url(r'^v1/userview/$', views.UserView.as_view()), # 通过get传递版本参数
    url(r'^(?P<version>[v1|v2]+)/userview/$', views.UserView.as_view()),# 通过url路径传递版本参数
    url(r'^(?P<version>[v1|v2]+)/parserview/$', views.ParserView.as_view()),# django rest的解析功能
]



