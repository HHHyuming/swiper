from django.http import HttpResponse
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import ValidationError


from user.models import User

class UserAuthentication(BaseAuthentication):

    def authenticate(self,request,*args,**kwargs):
        token=request.query_params.get('token')
        if not token:
            raise ValidationError('验证失败')
        user_id=int(token[-4:])
        user=User.objects.filter(id=1).first()
        request.user=user

        return user,token
