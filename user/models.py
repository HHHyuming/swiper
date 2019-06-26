from django.db import models

SEX = (
    (0, 'male'),
    (1, 'female')
)


# Create your models here.
class User(models.Model):
    phonenum = models.CharField(max_length=20, verbose_name='手机号')
    nickname = models.CharField(max_length=128, verbose_name='昵称')
    sex = models.CharField(max_length=16, choices=SEX, verbose_name='性别')
    birth_year = models.CharField(max_length=64, verbose_name='出生年')
    birth_month = models.CharField(max_length=64, verbose_name='出生月')
    birth_day = models.CharField(max_length=64, verbose_name='出生日')
    avatar = models.CharField(max_length=255, verbose_name='个人形象')
    location = models.CharField(max_length=255, verbose_name='常居地')

    @property
    def profile(self):
        profile_obj = Profile.objects.filter(id=self.id).first()
        return profile_obj


class Profile(models.Model):
    location = models.CharField(max_length=255, verbose_name='目标城市', null=True)
    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围', null=True)
    max_distance = models.IntegerField(default=50, verbose_name='最大查找范围', null=True)
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄', null=True)
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄', null=True)
    dating_sex = models.CharField(max_length=16, choices=SEX, verbose_name='匹配的性别', null=True)
    vibration = models.NullBooleanField(default=False, verbose_name='开启震动', null=True)
    only_matche = models.NullBooleanField(default=False, verbose_name='不让为匹配的人看我的相册', null=True)
    auto_play = models.NullBooleanField(default=False, verbose_name='自动播放视频', null=True)
