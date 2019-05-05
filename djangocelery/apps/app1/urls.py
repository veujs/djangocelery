# from django.contrib import admin
# from django.urls import path
from django.conf.urls import url, include
from apps.app1 import views

urlpatterns = [
    # path('admin/', admin.site.urls),  # 首此的登陆
    url(r'^v1/index_app1/$', views.index_app1),

    # 认证、限流、权限设置
    url(r'^(?P<version>[v1|v2]+)/auth/$', views.AuthView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/order/$', views.OrderView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/userinfo/$', views.UserInfoView.as_view()),


    # 序列化
    url(r'^(?P<version>[v1|v2]+)/roles/$', views.RolesView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/userinfo2/$', views.UserInfo2View.as_view()),
    url(r'^(?P<version>[v1|v2]+)/userinfo3/$', views.UserInfo3View.as_view()),
    url(r'^(?P<version>[v1|v2]+)/userinfo4/$', views.UserInfo4View.as_view()),

    # 在序列化的基础上，添加url来访问
    url(r'^(?P<version>[v1|v2]+)/group/(?P<ww>\d+)/$', views.GroupView.as_view(), name='gp'),

    # 序列化中的字段验证
    url(r'^(?P<version>[v1|v2]+)/usergroup/$', views.UserGroupView.as_view()),


    # url(r'^admin/', admin.site.urls),
    # url(r'^docs/', include_docs_urls(title='爬虫任务调度系统文档')),
    # url(r'^api/', include('apps.spiders.urls')),
    # url(r'^api/', include('apps.orders.urls')),
    # url(r'^api/', include('apps.source.urls')),
    # url(r'^api/', include('apps.verification.urls')),
    # url(r'^api/', include('apps.aliPay.urls')),
]



