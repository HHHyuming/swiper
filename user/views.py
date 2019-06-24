import random
from datetime import datetime


from rest_framework.decorators import list_route
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response,SimpleTemplateResponse
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer

from user.models import User
from user.serializer import *
from user.logic import send_shortmsg

# Create your views here.
# 登录 注册 发送邮件

class UserApiView(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        return Response({'code':200,'msg':'用户信息'})


    def create(self, request, *args, **kwargs):
        return Response({'code':200,'msg':'创建成功'})

    @list_route(methods=['GET'])
    def get_vcode(self,request,*args,**kwargs):
        # 发送短信
        phone = self.request.query_params.get('phone')
        code = random.sample(range(1000, 9999), 1)
        code_status = send_shortmsg(phone, code)
        if code_status!=1:
            return Response({'code':1001,'msg':'服务器繁忙请重试'})
        # 设置cookie/session 前端*
        # request.session['vcode']=code
        # return redirect(reverse('user:login'))
        return Response({'code':200,'msg':'发送成功','vcode':code,'code_time':datetime.now()})
    @list_route(methods=['POST'])
    def login(self, request, *args, **kwargs):

        # 校验验证码是否正确
        # 用户填写的vcode
        cur_vcode=self.request.data.get('vcode')
        # 获取session中的vcode进行对比
        # old_vcode=request.session.get('vcode')
        confirm_code=self.request.data.get('confirm_vcode')
        if cur_vcode!=confirm_code or not cur_vcode:
            return Response({'code':1002,'error':'验证码有误，请重新输入'})
        ser_obj=UserSerializer(instance=self.request.data,many=True)
        # 数据格式校验
        if ser_obj.is_valid():
            username=ser_obj.validated_data.get('username')
            password=ser_obj.validated_data.get('password')
            user_obj=User.objects.filter(username=username,password=password).first()
            if user_obj:
                return Response({'code':200,'msg':'登陆成功'})
            return Response({'code':1003,'msg':'账号或密码错误'})
        return Response({'code': 1004,'success_code':'数据格式校验失败'})

    @list_route(methods=['POST'])
    def register(self,request,*args,**kwargs):
        cur_vcode = self.request.data.get('vcode')
        # 获取session中的vcode进行对比
        # old_vcode=request.session.get('vcode')
        confirm_code = self.request.data.get('confirm_vcode')
        if cur_vcode != confirm_code or not cur_vcode:
            return Response({'code': 1002, 'error': '验证码有误，请重新输入'})

