import os
import random
from datetime import datetime

from django.core.cache import cache
from rest_framework.decorators import list_route
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (ListModelMixin, UpdateModelMixin)
from rest_framework.response import Response

from lib.authentication import UserAuthentication
from user.serializer import *
from user.logic import send_shortmsg, save_img
from utils.keys import VCODE, AVATAR_PATH
from django.conf import settings


# Create your views here.
# 登录 注册 发送邮件
from utils.user_sign import md5


class UserApiView(GenericViewSet, ListModelMixin, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [UserAuthentication,]

    def list(self, request, *args, **kwargs):

        user_obj = self.request.user

        ser = self.get_serializer(instance=user_obj.profile, many=False)

        return Response({'code': 200, 'data': ser.data})

    def update(self, request, *args, **kwargs):
        user_obj = self.request.user
        ser = self.get_serializer(data=request.data, many=False)
        if ser.is_valid():
            ser.save()
            return Response({'code': 200, 'msg': '用户信息修改成功'})
        print(ser.errors)
        return Response({'code': 1004, 'error': '数据格式错误'})

    @list_route(methods=['GET'],authentication_classes=[])
    def get_vcode(self, request, *args, **kwargs):
        # 发送短信
        phone = self.request.query_params.get('phone')
        code = random.sample(range(1000, 9999), 1)
        code_status = send_shortmsg.delay(phone,code)
        # if code_status != 1:
        #     return Response({'code': 1001, 'msg': '服务器繁忙请重试'})
        # 设置cookie/session 前端*
        # request.session['vcode']=code
        # 设置缓存
        key = VCODE % phone
        cache.set(key, code, 60 * 60)
        return Response({'code': 200, 'msg': '发送成功', 'vcode': code, 'code_time': datetime.now()})

    @list_route(methods=['POST'],authentication_classes=[])
    def login(self, request, *args, **kwargs):

        # 校验验证码是否正确
        # 用户填写的vcode
        cur_vcode = self.request.data.get('vcode')
        cur_phone = self.request.data.get('phone')
        # 获取session中的vcode进行对比
        # old_vcode=request.session.get('vcode')
        confirm_code = str(cache.get(VCODE % cur_phone)[0])
        print(confirm_code,cur_vcode)
        if cur_vcode != confirm_code or not cur_vcode:
            return Response({'code': 1002, 'error': '验证码有误，请重新输入'})
        # 数据格式校验
        user_obj = User.objects.filter(phonenum=cur_phone).first()
        if not user_obj:
            return Response({'code': 1005, 'error': '该用户不已存在'})
        # 签名
        sign_md5 = md5(user_id=user_obj.id)
        request.session['token'] = sign_md5 + str(0000 + user_obj.id)
        return Response({'code': 200, 'msg': '登陆成功'})

    @list_route(methods=['POST'],authentication_classes=[])
    def register(self, request, *args, **kwargs):
        cur_vcode = self.request.data.get('vcode')
        cur_phone = self.request.data.get('phone')
        # 从缓存中取出code
        confirm_code = str(cache.get(VCODE % cur_phone))
        if cur_vcode != confirm_code or not cur_vcode:
            return Response({'code': 1002, 'error': '验证码有误，请重新输入'})
        # 保存到数据库
        if User.objects.filter(phonenum=cur_phone).first():
            return Response({'code': 1005, 'error': '用户已存在'})
        User.objects.create(phonenum=cur_phone)
        return Response({"code": 200, 'msg': '注册成功'})

    @list_route(methods=['POST'],authentication_classes=[])
    def upload_img(self, request, *args):
        try:
            user=self.request.user
            avatar = self.request.FILES.get('avatar')
            save_img.delay(avatar,user)
            # filename = os.path.join(settings.MEDIA_ROOT, AVATAR_PATH%self.request.user.id)
            # with open(filename, 'wb+')as f:
            #     for chunk in avatar.chunks():
            #         f.write(chunk)
        except Exception as e:
            return Response({'code': 1006, 'msg': f'文件上传失败{e}'})
        return Response({'code': 200, 'msg': '上传文件成功'})
