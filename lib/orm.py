"""
猴子补丁
"""
from django.core.cache import cache
from django.db.models import Model
from utils import keys


# TODO

def get(cls, *args, **kwargs):
    "从缓存中拿 拿不到从数据库中拿"
    pk = kwargs.get('id') or kwargs.get('pk')
    if not pk:
        data = cls.objects.create(*args, **kwargs)
        return data
    key = keys.OBJPK % pk
    data = cache.get(key)
    if not data:
        data = cls.objects.get(pk=pk)
        cache.set(key, data)
    return data


def get_or_create(cls,*args,**kwargs):
    "从缓存中拿 拿不到从数据库中创建"
    pk = kwargs.get('id') or kwargs.get('pk')
    if not pk:
        data,created = cls.objects.get_or_create(*args, **kwargs)
        return data
    key = keys.OBJPK % pk
    data = cache.get(key)
    if not data:
        data = cls.objects.get_or_create(pk=pk)
        cache.set(key, data)
    return data


def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    "创建实例对象 然后存入缓存 "
    self.new_save()
    key = keys.OBJPK % self.id
    cache.set(key, self, 86400 * 15)


def model_patch():
    "给Model绑定 缓存方法"
    Model.get=classmethod(get)
    Model.get_or_create=classmethod(get_or_create)
    Model.new_save=Model.save
    Model.save=save