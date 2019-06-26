from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    """用户序列化与数据格式校验"""

    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"

    def validate(self, attrs):
        print(attrs)
        if attrs['min_distance']>attrs['max_distance']:
            raise ValidationError("最大距离小于最小距离")
        return attrs

