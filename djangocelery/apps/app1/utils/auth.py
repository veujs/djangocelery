
from apps.app1 import models
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, BasicAuthentication

class FirstAuthtication(BaseAuthentication):
    def authenticate(self, request):
        pass

    # 注意：这个函数内部没有进行任何操作，但是如果通过自己写authentication_classes中的类的话，下面的函数必须添加
    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass


class Authtication(BaseAuthentication):

    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败！')
        # 在rest_framework内部中会将两个字段赋值给request，供后续操作使用
        return (token_obj.user,token_obj)

    # 注意：这个函数内部没有进行任何操作，但是如果通过自己写authentication_classes中的类的话，下面的函数必须添加
    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass



