from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from apps.app1 import models
from apps.app1.utils.auth import *
# Create your views here.
from apps.app1.utils.permissions import Mypermission, Mypermission2
from apps.app1.utils.throttle import *
import json

import logging

# logger = logging.getLogger('django.request')
logger = logging.getLogger(__name__)



def index(request):
    return render(request, 'index.html')


def index_app1(request):
    logger.info("1231231231231231233123123")
    logger.info(logger.name)
    logger.debug("00000000000000000000000000000000")
    logger.warning("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
    print(logger.name)
    logger.error("5656565656565656565656565")
    return render(request, 'index_app1.html')



def md5(user):
    import hashlib
    import time
    ctime = str(time.time())

    m = hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))
    return m.hexdigest()

class AuthView(APIView):
    """
    用户登陆功能
    """
    authentication_classes = []  # 通过设置为空列表，使得当前请求不进行认证的功能
    permission_classes = []  # 不进行权限认证
    throttle_classes = [VisitThrottle2,]  # 匿名用户节流限制
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            print(user, pwd)
            obj = models.UserInfo.objects.filter(username=user,password=pwd).first()
            print(obj)
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'

            # 为登陆用户创建token
            token = md5(user)
            print(token)
            # 存在则更新，不存在就创建
            models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = "请求异常"

        return JsonResponse(ret)

ORDER_DICT = {
    1: {
        'name': "小鸡",
        'age': 13,
        'gender': '男'
    },
    2: {
        'name': "小鸭",
        'age': 16,
        'gender': '女'
    }
}

class OrderView(APIView):
    '''
    订单管理
        1、需要带token认证
        2、设置权限限制 Mypermission
        3、使用登陆用户限流控制 UserThrottle
    '''
    # 认证类集合
    authentication_classes = [Authtication, ]  # 注意  在dispatch函数中进行认证的
    # 权限类集合
    permission_classes = [Mypermission,]
    # 访问频率的控制
    throttle_classes = [UserThrottle,]  # 登陆用户节流限制

    def get(self, request, *args, **kwargs):
        self.dispatch
        token = request._request.GET.get('token')

        if not token:
            return HttpResponse('用户为登陆！！')
        ret = {'code': 1000, 'msg': None, 'token': token}

        # 自定义访问的权限
        if request.user.user_type == '3':
            return HttpResponse("无权访问")

        try:
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)


class UserInfoView(APIView):
    """
    用户信息访问：
        1、需要带token认证
        2、不设置权限限制
        3、使用登陆用户限流控制
    """
    # 认证类集合
    authentication_classes = [Authtication,] #  注意  在dispatch函数中进行认证的
    # 权限类集合
    permission_classes = []
    # 访问频率的控制
    throttle_classes = [UserThrottle,]  # 登陆用户节流限制
    def get(self,request, *args, **kwargs):

        # 自定义访问的权限
        if request.user.user_type == 3:
            return HttpResponse("无权访问")
        return HttpResponse("用户信息")


# #--------------序列化的实现方法------------------------##

# 序列化1--简单实现
from rest_framework import serializers
class RolesSerializer(serializers.Serializer):
    title = serializers.CharField()

class RolesView(APIView):
    """django从数据库中取出的是Queryset类型，不能用json直接进行序列化"""
    # authentication_classes = []
    def get(self, request, *args, **kwargs):
        # 方式1
        # roles = models.Role.objects.all().values('id','title')
        # roles = list(roles)
        # ret = json.dumps(roles,ensure_ascii=False)
        # 方式2:将Queryset类型的数据，利用rest的序列化器，将数据类型进行转化为[obj1,obj2,obj3]
        roles = models.Role.objects.all()
        ser = RolesSerializer(instance=roles,many=True)
        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)


# 序列化2--基于serializers.Serializer简单实现+功能添加
# 对于字段中含有ChOICE这种类型的字段可以使用soource参数  or 自定义方法来取数据
class UserInfo2Serializer(serializers.Serializer):
    # user_type = serializers.IntegerField()
    oooo = serializers.CharField(source="user_type")# row.get_user_type_display  作用是对user_type起个别名 oooo
    username = serializers.CharField()
    password = serializers.CharField()

    gp = serializers.CharField(source='groupp.title')
    #rls = serializers.CharField(source='roles.all')  # 此时使用source的方法可能行不通，可以采用下面的方式
    rls = serializers.SerializerMethodField() # 自定义显示,结合下面的get方法

    def get_rls(self,row):
        role_obj_list = row.role.all()
        ret = []
        for item in role_obj_list:
            ret.append({'id':item.id,'title':item.title})
        return ret


class UserInfo2View(APIView):
    def get(self, request, *args, **kwargs):
        users = models.UserInfo.objects.all()
        ser = UserInfo2Serializer(instance=users,many=True)
        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)


# 序列化3--基于serializers.ModelSerializer类实现序列化
# 使用serializers.ModelSerializer，可以结合数据库，帮助用户快速序列化，但是仍可以自定义来完善字段内容
class UserInfo3Serializer(serializers.ModelSerializer):
    oooo = serializers.CharField(source='get_user_type_display')
    rls = serializers.SerializerMethodField()# 自定义显示,结合下面的get方法
    class Meta:
        model = models.UserInfo
        # fields = '__all__'  # 使用这种方法，出现关联性数据，以及CHOICE字段的时候只能显示id，其他信息显示不全
        fields = ['id', 'username','password','oooo','rls','groupp']
        # extra_kwargs = {'groupp':{'source':'groupp.title'},}  # 表示在上边生成group字段的时候，利用extra_kwargs生成更详细的内容（先忽略，有问题！！！）
    # oooo以及rls为自定义的字段名
    def get_rls(self,row):
        role_obj_list = row.role.all()
        ret = []
        for item in role_obj_list:
            ret.append({'id':item.id,'title':item.title})
        return ret
class UserInfo3View(APIView):
    def get(self,request, *args, **kwargs):
        users = models.UserInfo.objects.all()
        ser = UserInfo3Serializer(instance=users,many=True)
        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)


# 序列化4--基于serializers.ModelSerializer类实现序列化，使用元类中的depth字段
# 使用serializers.ModelSerializer,中的元类里面的depth，可以完成上边的操作，嵌套的查询数据库中的字段内容
class UserInfo4Serializer(serializers.ModelSerializer):
    groupp = serializers.HyperlinkedIdentityField(view_name='gp',lookup_field='groupp_id',lookup_url_kwarg='ww')
    class Meta:
        model = models.UserInfo
        fields = '__all__'  # 使用这种方法，出现关联性数据，以及CHOICE字段的时候只能显示id，其他信息显示不全
        depth = 1

class UserInfo4View(APIView):
    def get(self,request, *args, **kwargs):
        users = models.UserInfo.objects.all()
        ser = UserInfo4Serializer(instance=users,many=True,context={'request': request})
        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserGroup
        fields = '__all__'  # 使用这种方法，出现关联性数据，以及CHOICE字段的时候只能显示id，其他信息显示不全
        # depth = 2

class GroupView(APIView):
    def get(self,request, *args, **kwargs):
        ww = self.kwargs.get('ww')
        obj = models.UserGroup.objects.filter(pk=ww).first()
        ser = GroupSerializer(instance=obj,many=False)
        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)




# 序列化中字段验证的实现--1-字段参数   2--钩子函数
class xxxvalidator(object):
    def __init__(self,base):
        self.base = base
    def __call__(self, value):
        if not value.startswith('luffy'):
            message = '标题必须为 %s 为开头' % self.base
            raise serializers.ValidationError(message)

class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(error_messages={'required':'标题不能为空！'},validators=[xxxvalidator('luffy'),])

class UserGroupView(APIView):

    def post(self,request,*args,**kwargs):
        ser = UserGroupSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data['title'])
        else:
            print(ser.errors)
        return HttpResponse('提交数据')




# 分页功能1--基于PageNumberPagination类的分页实现
class PagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = "__all__"

from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response
class Pager1View(APIView):

    def get(self,request,*args,**kwargs):
        roles = models.Role.objects.all()
        pg = PageNumberPagination()
        pg_roles = pg.paginate_queryset(queryset=roles,request=request,view=self)
        print(pg_roles)
        ser = PagerSerializer(instance=pg_roles,many=True)
        # ret = json.dumps(ser.data,ensure_ascii=False)ss
        # return Response(ret)
        return Response(ser.data)




# 分页功能2--基于LimitOffsetPagination类的分页实现
from rest_framework.pagination import LimitOffsetPagination
class MyPagination(LimitOffsetPagination):

    default_limit = 2 # page_size设置为2，如果不设置，就默认为settings中设置的PAGE_SIZE大小
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 5

from rest_framework.response import Response
class Pager2View(APIView):

    def get(self,request,*args,**kwargs):
        roles = models.Role.objects.all()
        pg = MyPagination()
        pg_roles = pg.paginate_queryset(queryset=roles,request=request,view=self)
        # print(pg_roles)
        ser = PagerSerializer(instance=pg_roles,many=True)
        # ret = json.dumps(ser.data,ensure_ascii=False)ss
        # return Response(ret)
        return Response(ser.data)

# 分页功能3--基于CursorPagination类的分页实现
from rest_framework.pagination import CursorPagination
class MyPagination3(CursorPagination):

    cursor_query_param = 'cursor'
    page_size = 2
    ordering = 'id'

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = None
    max_page_size = 5

from rest_framework.response import Response
class Pager3View(APIView):

    def get(self,request,*args,**kwargs):
        roles = models.Role.objects.all()
        pg = MyPagination3()
        pg_roles = pg.paginate_queryset(queryset=roles,request=request,view=self)
        # print(pg_roles)
        ser = PagerSerializer(instance=pg_roles,many=True)
        # ret = json.dumps(ser.data,ensure_ascii=False)ss
        # return Response(ret)
        # return Response(ser.data)
        return pg.get_paginated_response(ser.data)



# 视图-基于GenericAPIView类实现（不常用）
from rest_framework.generics import GenericAPIView
class GenericView(GenericAPIView):

    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination

    def get(self,request, *args, **kwargs):
        # 获取数据
        roles = self.get_queryset() # 获取上边的queryset
        # 分页
        pager_roles = self.paginate_queryset(roles)
        # 序列化
        ser = self.get_serializer(instance=pager_roles,many=True)

        return Response(ser.data)

# 视图 - 基于GenericViewset类实现
from rest_framework.viewsets import GenericViewSet
class GenericViewsetView(GenericViewSet):

    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination

    def list(self,request, *args, **kwargs):
        # 获取数据
        roles = self.get_queryset() # 获取上边的queryset
        # 分页
        pager_roles = self.paginate_queryset(roles)
        # 序列化
        ser = self.get_serializer(instance=pager_roles,many=True)

        return Response(ser.data)


# 视图 - 基于ModelViewSet类实现
from rest_framework.viewsets import ModelViewSet
class ModelViewsetView(ModelViewSet):

    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination

    # def list(self,request, *args, **kwargs):
    #     # 获取数据
    #     roles = self.get_queryset() # 获取上边的queryset
    #     # 分页
    #     pager_roles = self.paginate_queryset(roles)
    #     # 序列化
    #     ser = self.get_serializer(instance=pager_roles,many=True)
    #
    #     return Response(ser.data)

















