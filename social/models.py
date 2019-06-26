from django.db import models


# Create your models here.

class Swiped(models.Model):
    uid = models.IntegerField(verbose_name='用户自身id')
    sid = models.IntegerField(verbose_name='被滑的陌生人')
    mark = models.CharField(max_length=64, verbose_name='滑动类型time滑动的时间id')
    time = models.DateTimeField(auto_now_add=True, verbose_name='滑动的时间')

    class Meta:
        unique_together = (('uid', 'sid'),)

class Friend(models.Model):
    uid1 = models.IntegerField(verbose_name='好友ID')
    uid2 = models.IntegerField(verbose_name='友ID')

    class Meta:
        unique_together = (('uid1', 'uid2'),)
