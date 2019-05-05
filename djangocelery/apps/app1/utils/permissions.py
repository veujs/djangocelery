
from rest_framework.permissions import BasePermission

class Mypermission(BasePermission):

    def has_permission(self, request, view):
        # print(request.user.user_type)
        if request.user.user_type != "1":
            return False  # 允许访问
        return True # 不允许访问
class Mypermission2(BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type == "3":
            return False
        return True




