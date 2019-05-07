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

    # 序列化中的字段验证测试
    url(r'^(?P<version>[v1|v2]+)/usergroup/$', views.UserGroupView.as_view()),


    # 分页测试
    # 分页测试-基于PageNumberPagination类实现分页
    url(r'^(?P<version>[v1|v2]+)/pager1/$', views.Pager1View.as_view()),

    # 分页测试-基于LimitOffsetPagination类实现分页
    url(r'^(?P<version>[v1|v2]+)/pager2/$', views.Pager2View.as_view()),

    # 分页测试-CursorPagination类实现分页,url中页码参数加密
    url(r'^(?P<version>[v1|v2]+)/pager3/$', views.Pager3View.as_view()),

    # 视图 - 基于GenericAPIView类实现（不常用）
    url(r'^(?P<version>[v1|v2]+)/generic/$', views.GenericView.as_view()),

    # 视图 - 基于GenericViewset类实现  注意：从这里开始  url中as_view()中需要额外指定method，类似于{'get':'list','post':'create'}
    url(r'^(?P<version>[v1|v2]+)/genericviewset/$', views.GenericViewsetView.as_view({'get': 'list'})),

    # 视图 - 基于ModelViewset类实现  注意：从这里开始  url中as_view()中需要额外指定method，类似于{'get':'list','post':'create'}
    url(r'^(?P<version>[v1|v2]+)/modelviewset/$', views.ModelViewsetView.as_view({'get': 'list','post':'create'})),
    url(r'^(?P<version>[v1|v2]+)/modelviewset\.(?P<format>[\w]+)$', views.ModelViewsetView.as_view({'get': 'list','post':'create'})),


    url(r'^(?P<version>[v1|v2]+)/modelviewset/(?P<pk>[\w]+)/$', views.ModelViewsetView.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update', 'patch': 'partial_update'})),
    url(r'^(?P<version>[v1|v2]+)/modelviewset/(?P<pk>[\w]+)\.(?P<format>[\w]+)$', views.ModelViewsetView.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update', 'patch': 'partial_update'})),

]



