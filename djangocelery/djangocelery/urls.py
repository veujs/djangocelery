"""djangocelery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from apps.app1 import views
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),  # 首此的登陆
    url(r'^docs/', include_docs_urls(title='爬虫任务调度系统文档')),

    url(r'^$', views.index),
    url(r'^api/', include('apps.app1.urls')),
    url(r'^api/', include('apps.app2.urls')),

    # url(r'^admin/', admin.site.urls),
    # url(r'^docs/', include_docs_urls(title='爬虫任务调度系统文档')),
    # url(r'^api/', include('apps.spiders.urls')),
    # url(r'^api/', include('apps.orders.urls')),
    # url(r'^api/', include('apps.source.urls')),
    # url(r'^api/', include('apps.verification.urls')),
    # url(r'^api/', include('apps.aliPay.urls')),
]

