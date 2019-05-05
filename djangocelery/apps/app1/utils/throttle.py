import time
from rest_framework.throttling import BaseThrottle
from rest_framework.throttling import SimpleRateThrottle, ScopedRateThrottle
VISIT_RECODE = {}  #  原则上来说，这个全局变量需要放在缓存中防止重启丢失
class VisitThrottle(object):
    """自定义实现匿名用户的访问控制--根据ip来实现登陆记录"""
    def __init__(self):
        self.history = None

    def allow_request(self,request,view):
        # 1.首先获取用户ip
        remote_addr = request._request.META.get("REMOTE_ADDR")
        ctime = time.time()

        # print(remote_addr)
        # print(VISIT_RECODE)
        if remote_addr not in VISIT_RECODE:
            VISIT_RECODE[remote_addr] = [ctime,]
            print("recode:", VISIT_RECODE)
            return True

        history = VISIT_RECODE.get(remote_addr)

        self.history = history
        while history and history[-1] < ctime - 60:
            history.pop()
        print("recode:",VISIT_RECODE)
        if len(history) < 3:
            history.insert(0,ctime)
            print("recode:", VISIT_RECODE)
            return True
        # return True # False 表示访问频率过高，被限制
        # return False

    def wait(self): # 表示还需要等待多久才能继续访问
        ctime = time.time()
        return 60 - (ctime - self.history[-1])


class VisitThrottle2(SimpleRateThrottle):
    """利用SimpleRateThrottle类实现匿名用户的访问频率控制"""
    scope = "wzp" # wzp为匿名用户的频率限制

    def get_cache_key(self, request, view):
        """源码中此方法里面是空的，需要自己重新写的！！，（对缓存的处理）"""
        """此方法是必须进行重写---返回匿名用户ip"""
        return self.get_ident(request)


class UserThrottle(SimpleRateThrottle):
    """利用SimpleRateThrottle类实现登陆用户的访问频率控制"""
    scope = 'wzp01' # wzp01为登陆用户的频率限制

    def get_cache_key(self, request, view):
        return request.user.username
