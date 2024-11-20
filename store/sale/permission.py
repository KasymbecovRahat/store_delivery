from rest_framework.permissions import BasePermission
from .views import permissions

class CheckOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 'Владелец':
            return False
        return True


class CheckCrud(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.user_role == 'Владелец'