from django.core.cache import cache
from django.middleware.http import MiddlewareMixin

from user.models import User

class MyMiddlerMixin(MiddlewareMixin):

    def process_request(self,request,*args,**kwargs):


        #
        # WHITE_URL=['/api/users/user/login/','/api/users/user/register/']
        # if request.path in WHITE_URL:
        #     return
        # token=request.POST.get('token')
        #
        # if not token:
        #     raise HttpResponse({'验证失败'})
        # user_id=int(token[-4:])
        # user=User.objects.filter(id=user_id).first()
        # return user,token
        return
# class UserAuthentication(BaseAuthentication):
#     WHITE_URL=['/api/users/user/login/','/api/users/user/register/']
#
#     def authenticate(self,request,*args,**kwargs):
#         token=request.data.get('token')
#
#         if not token:
#             raise ValidationError('验证失败')
#         user_id=int(token[-4:])
#         user=User.objects.filter(id=user_id).first()
#         return user,token
