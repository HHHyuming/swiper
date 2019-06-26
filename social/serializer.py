from rest_framework import serializers

from social.models import Swiped, Friend


class SwipedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swiped
        fields = '__all__'


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__'

    # def to_representation(self, instance):
    #     res = super(FriendSerializer, self).to_representation(instance)
    #     print(res)
    #     return
