import datetime

from django.core.cache import cache
from django.db.models import Q
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
# Create your views here.
from lib.userpermission import UserPermission
from social.models import Swiped, Friend
from social.serializer import SwipedSerializer, FriendSerializer
from user.models import User
from user.serializer import UserSerializer
from utils.keys import REGRET_USERID, TOP_N, \
    LIKE_KEY, LIKE_SOCRE, SUPER_LIKE_SCORE, DISLIKE_SCORE, LIKE_RANK

from lib.cache import rds


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
            try:
                test_obj = Swiped.objects.create(uid=uid, sid=sid, mark='like')
                print(test_obj)
                # TODO
                uid, sid = (uid, sid) if int(uid) < int(sid) else (sid, uid)
                Friend.objects.create(uid1=uid, uid2=sid)
                # 满意+5
                rds.zincrby(LIKE_RANK, LIKE_KEY % sid, LIKE_SOCRE)
            except Exception as e:
                return Response({'code': 500, 'msg': '错误'})
            return Response({'code': 200})

        test_obj, created = Swiped.objects.get_or_create(uid=uid, sid=sid, mark='like')
        ser = self.get_serializer(test_obj, many=False)
        rds.zincrby(LIKE_RANK, LIKE_KEY % sid, LIKE_SOCRE)

        return Response({'code': 200, 'data': ser.data})

    @list_route(methods=['POST'], permission_classes=[UserPermission, ])
    def superlike(self, request, *args, **kwargs):
        uid = self.request.data.get('uid')
        sid = self.request.data.get('sid')
        like_flag_obj = Swiped.objects.filter(uid=sid, sid=uid, mark__in=['like', 'superlike']).exists()
        # 查看对方是否也喜欢自己
        if like_flag_obj:
            try:
                test_obj = Swiped.objects.create(uid=uid, sid=sid, mark='superlike')
                print(test_obj)
                # TODO
                uid, sid = (uid, sid) if int(uid) < int(sid) else (sid, uid)
                Friend.objects.create(uid1=uid, uid2=sid)
                rds.zincrby(LIKE_RANK, LIKE_KEY % sid, SUPER_LIKE_SCORE)

            except Exception:
                return Response({'code': 500, 'msg': '错误'})
            return Response({'code': 200, 'msg': '成功'})

        test_obj, created = Swiped.objects.get_or_create(uid=uid, sid=sid, mark='superlike')

        ser = self.get_serializer(test_obj, many=False)
        rds.zincrby(LIKE_RANK, LIKE_KEY % sid, SUPER_LIKE_SCORE)

        return Response({'code': 200, 'data': ser.data})

    @list_route(methods=['POST'])
    def dislike(self, request, *args, **kwargs):
        user_id = request.user.id
        user_id = self.request.data.get('uid')
        sid = self.request.data.get('sid')
        delete_obj = Swiped.objects.filter(uid=user_id, sid=sid).delete()
        rds.zincrby(LIKE_RANK, LIKE_KEY % sid, DISLIKE_SCORE)

        return Response({'code': 200, 'msg': '操作成功'})

    @list_route(methods=['POST'], permission_classes=[UserPermission, ])
    def regret(self, request, *args, **kwargs):
        user = request.user
        regret_counts = cache.get(REGRET_USERID % user.id, 0)
        if regret_counts < 3:
            # 获取当前时间
            now = datetime.datetime.now()
            cache_time = 86000 - (now.hour * 3600 + now.minute * 60 + now.second)
            print(user)
            latest_time = Swiped.objects.filter(uid=user.id).latest(field_name='time')
            # 删除解除好友关系
            # 判断是否有好友关系
            uid1, uid2 = (user.id, latest_time.sid) if user.id < latest_time.sid else (latest_time.sid, user.id)
            friends = Friend.objects.filter(uid1=uid1, uid2=uid2)
            friends.delete()
            latest_time.delete()
            regret_counts += 1
            cache.set(REGRET_USERID % user.id, regret_counts, timeout=cache_time)
            return Response({'code': 200, 'msg': '后悔操作成功'})
        return Response({'code': 1006, 'error': '次数已达上限'})

    @list_route(methods=['GET'], permission_classes=[UserPermission, ])
    def liked_me(self, request, *args, **kwargs):
        user_id = self.request.user.id
        like_me_list = Swiped.objects.filter(sid=user_id, mark__in=['like', 'superlike'])
        serializer = self.get_serializer(like_me_list, many=True)

        return Response({'code': 200, 'data': {'msg': 'SUCCESS', 'data': serializer.data}})

    @list_route(methods=['GET'])
    def rank_top(self, request, *args, **kwargs):
        """排名"""
        # 排名列表
        rank_list = rds.zrevrange('LIKE_RANK', 0, -1, withscores=True)
        rank_list = [[int(i), int(k)] for i, k in rank_list]
        rank_list = list(sorted(rank_list, key=lambda x: -x[0]))
        print(rank_list)
        rank_id = [j[1] for j in rank_list]
        # 查询在rank里面的用户
        user_list = User.objects.filter(id__in=rank_id)
        # 排行榜数据
        users = list(sorted(user_list, key=lambda x: rank_id.index(x.id)))
        data = []
        for rank, (score, _), user_obj in zip(range(1, TOP_N + 1), rank_list, users):
            temp_dic = {
                'rank': rank,
                'score': score,
                'user': UserSerializer(user_obj, many=False).data
            }
            data.append(temp_dic)
        return Response({'code': 200, 'data': data})


# 1. 交友模块
#    - 获取推荐列表
#    - 喜欢 / 超级喜欢 / 不喜欢
#    - 反悔 (每天允许返回 3 次)
#    - 查看喜欢过我的人

# 2. 好友模块
#    - 查看好友列表
#    - 查看好友信息


class FriendAPIView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    # def xx(self):
    #     if issubclass()
    def list(self, request, *args, **kwargs):
        user_id = self.request.user.id
        user_id = 1
        my_friend = Friend.objects.filter(Q(uid1=user_id) | Q(uid2=user_id)).values('uid1', 'uid2')
        nickname_list = [User.objects.get(id=obj['uid1']).nickname for obj in my_friend if obj['uid1'] != user_id] \
            .extend([User.objects.get(id=obj['uid2']).nickname for obj in my_friend if obj['uid2'] != user_id])
        # return Response({'code':200,'data':friend_list.data})
        print(nickname_list)
        return Response({'code': 200, 'data': nickname_list})
    #
    # def retrieve(self, request, *args, **kwargs):
    #     self.get_object()
