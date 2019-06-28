from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from vip.models import VipPermission, Permission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        path = request.path
        user = request.user
        # 当前权限对象
        per_obj = Permission.objects.get(url=path)
        # 用户所拥有的权限
        permission_list = VipPermission.objects.filter(vip_id=3)
        per_id_list = [i.per_id for i in permission_list]

        if per_obj.id not in per_id_list:
            raise PermissionDenied('没有权限，请前往充值')
        return True
