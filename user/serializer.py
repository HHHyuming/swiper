from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """用户序列化与数据格式校验"""
    class Meta:
        model = User
        fields = '__all__'
