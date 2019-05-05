from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.versioning import BaseVersioning
# from django.http import HttpResponse
# Create your views here.
def index_app2(request):
    # return HttpResponse("asdfasdfa")
    return render(request,'index_app2.html')
"""
# 根据源码自定义实现url中的版本获取
from rest_framework.versioning import BaseVersioning
class ParamVersion(BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        version = request.query_params.get("version")
        return version

class UserView(APIView):
    authentication_classes = []  # 通过设置为空列表，使得当前请求不进行认证的功能
    permission_classes = []  # 不进行权限认证
    throttle_classes = []  # 不进行限流
    versioning_class = ParamVersion
    def get(self,request,*args,**kwargs):
        # version = request._request.GET.get("version")
        # version = request.query_params.get("version")
        version = request.version
        return HttpResponse(version)
"""

"""
#直接使用内置方法获取url中get传递的版本号
from rest_framework.versioning import QueryParameterVersioning
class UserView(APIView):
    authentication_classes = []  # 通过设置为空列表，使得当前请求不进行认证的功能
    permission_classes = []  # 不进行权限认证
    throttle_classes = []  # 不进行限流
    versioning_class = QueryParameterVersioning
    def get(self,request,*args,**kwargs):
        version = request.version
        return HttpResponse(version)
"""
"""直接使用内置方法获取url的路径中传递的版本号"""
from rest_framework.versioning import URLPathVersioning
class UserView(APIView):
    authentication_classes = []  # 通过设置为空列表，使得当前请求不进行认证的功能
    permission_classes = []  # 不进行权限认证
    throttle_classes = []  # 不进行限流
    # versioning_class = URLPathVersioning
    def get(self,request,*args,**kwargs):
        version = request.version
        return HttpResponse(version)


# restframework的解析  注意区别于django自带的解析
from rest_framework.parsers import JSONParser,FormParser
class ParserView(APIView):
    authentication_classes = []  # 通过设置为空列表，使得当前请求不进行认证的功能
    permission_classes = []  # 不进行权限认证
    throttle_classes = []  # 不进行限流
    # versioning_class = URLPathVersioning
    parser_classes = [JSONParser,FormParser]
    def post(self,request,*args,**kwargs):
        """
        1、JSONParser，表示允许用户发送json格式数据
            a:content-type :'application/json'
            b:{"name":"wzp","age":18}
        2、FormParser，表示允许用户发送json格式数据
            a:content-type :'application/x-www-form-urlencoded'
            b:{"name":"wzp","age":18}
        :param request:
        :param args:
        :param kwargs:
        :return:s
        """
        print(type(request.data))
        print(request.data)
        return HttpResponse("ok")





