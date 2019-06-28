from django.db import models


# Create your models here.

class VipModel(models.Model):
    name = models.CharField(max_length=64, verbose_name='会员名称')
    level = models.IntegerField(default=0, verbose_name='登记')
    price = models.FloatField(verbose_name='价格')


class Permission(models.Model):
    name = models.CharField(max_length=64, verbose_name='权限名称')
    description = models.TextField(verbose_name='权限说明')
    url = models.CharField(max_length=128,verbose_name='权限路由')

class VipPermission(models.Model):
    vip_id = models.IntegerField()
    per_id = models.IntegerField()
