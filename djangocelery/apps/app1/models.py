from django.db import models
# Create your models here.
class UserGroup(models.Model):
    title = models.CharField(max_length=32)

class Role(models.Model):
    title = models.CharField(max_length=32)


class UserInfo(models.Model):
    user_type_choices = (
        (1, '普通用户'),
        (2, 'vip'),
        (3, 'vvip'),

    )
    user_type = models.CharField(max_length=32, choices=user_type_choices)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)

    role = models.ManyToManyField("Role")
    groupp = models.ForeignKey("UserGroup",on_delete=True)

class UserToken(models.Model):

    user = models.OneToOneField(to="UserInfo", on_delete=True)
    token = models.CharField(max_length=64)




