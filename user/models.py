from django.db import models

# Create your models here.
class User(models.Model):
    SEX=(
        (0,'male'),
        (1,'female')
    )
    phonenum=models.CharField(max_length=20,verbose_name='手机号')
    nickname=models.CharField(max_length=128,verbose_name='昵称')
    sex= models.CharField(max_length=16,choices=SEX,verbose_name='性别')
    birth_year=models.CharField(max_length=64,verbose_name='出生年')
    birth_month = models.CharField(max_length=64,verbose_name='出生月')
    birth_day=models.CharField(max_length=64,verbose_name='出生日')
    avatar=models.CharField(max_length=255,verbose_name='个人形象')
    location=models.CharField(max_length=255,verbose_name='常居地')