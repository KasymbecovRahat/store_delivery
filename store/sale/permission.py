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


class CheckClientOrders(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.client_orders


class CheckOwnerStore(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class CheckOrders(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.orders_status == 'Ожидает  обработки':
            return True
        return False


class CheckClient(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.user_role == obj.client_orders











