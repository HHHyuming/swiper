import datetime

from django.core.cache import cache
from django.db.models import Q
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
# Create your views here.
from social.models import Swiped, Friend
from social.serializer import SwipedSerializer, FriendSerializer
from utils.keys import REGRET_USERID

class SocialAPIView(GenericViewSet, ListModelMixin):
    queryset = Swiped.objects.all()
    serializer_class = SwipedSerializer

    def list(self, request, *args, **kwargs):
        user_id = self.request.user.id
        all_swiped = Swiped.objects.filter(uid=user_id).all()
        ser = SwipedSerializer(all_swiped, many=True)
        return Response({'code': 200, 'data': ser.data})

    @list_route(methods=['POST'])
    def like(self, request, *args, **kwargs):
        uid = self.request.data.get('uid')
        sid = self.request.data.get('sid')
        like_flag_obj = Swiped.objects.filter(uid=sid, sid=uid, mark__in=['like', 'superlike']).exists()
        # 查看对方是否也喜欢自己
        if like_flag_obj:
            test_obj = Swiped.objects.create(uid=uid, sid=sid, mark='like')
            print(test_obj)
            # TODO
            uid, sid = (uid, sid) if int(uid) < int(sid) else (sid, uid)
            Friend.objects.create(uid1=uid, uid2=sid)
            return

        test_obj = Swiped.objects.create(uid=uid, sid=sid, mark='like')
        ser = self.get_serializer(test_obj, many=False)
        return Response({'code': 200, 'data': ser.data})

    @list_route(methods=['POST'])
    def superlike(self, request, *args, **kwargs):
        uid = self.request.data.get('uid')
        sid = self.request.data.get('sid')
        like_flag_obj = Swiped.objects.filter(uid=sid, sid=uid, mark__in=['like', 'superlike']).exists()
        # 查看对方是否也喜欢自己
        if like_flag_obj:
            test_obj = Swiped.objects.create(uid=uid, sid=sid, mark='superlike')
            print(test_obj)
            # TODO
            uid, sid = (uid, sid) if int(uid) < int(sid) else (sid, uid)
            Friend.objects.create(uid1=uid, uid2=sid)
            return

        test_obj = Swiped.objects.create(uid=uid, sid=sid, mark='superlike')
        ser = self.get_serializer(test_obj, many=False)
        return Response({'code': 200, 'data': ser.data})

    @list_route(methods=['POST'])
    def dislike(self, request, *args, **kwargs):
        user_id = request.user.id
        sid = self.request.data.get('sid')
        delete_obj = Swiped.objects.filter(uid=user_id, sid=sid).delete()
        return Response({'code': 200, 'msg': f'操作成功{delete_obj}'})

    def regret(self, request, *args, **kwargs):
        user = request.user
        regret_counts=cache.get(REGRET_USERID%user.id,0)
        if regret_counts <3:
            # 获取当前时间
            now=datetime.datetime.now()
            cache_time =86000 - (now.hour*3600 + now.minute*60 + now.second)

            latest_time = Swiped.objects.filter(uid=user.id).latest(field_name='time')
            # 删除解除好友关系
            # 判断是否有好友关系
            uid1, uid2 = (user.id, latest_time.sid) if user.id < latest_time.sid else (latest_time.sid, user.id)
            friends = Friend.objects.filter(uid1=uid1, uid2=uid2)
            friends.delete()
            latest_time.delete()
            regret_counts += 1
            cache.set(REGRET_USERID%user.id,regret_counts,timeout=cache_time)
            return Response({'code':200,'msg':'后悔操作成功'})
        return Response({'code':1006,'error':'次数已达上限'})
# 1. 交友模块
#    - 获取推荐列表
#    - 喜欢 / 超级喜欢 / 不喜欢
#    - 反悔 (每天允许返回 3 次)
#    - 查看喜欢过我的人

# 2. 好友模块
#    - 查看好友列表
#    - 查看好友信息


class FriendAPIView(GenericViewSet,ListModelMixin,RetrieveModelMixin):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    # def list(self, request, *args, **kwargs):
    #     user_id=self.request.user.id
    #     my_friend=Friend.objects.filter(Q(uid1=user_id) |Q(uid2=user_id)).all()
    #     friend_list=FriendSerializer(my_friend,many=True)
    #     return Response({'code':200,'data':friend_list.data})
    #
    # def retrieve(self, request, *args, **kwargs):
    #     self.get_object()