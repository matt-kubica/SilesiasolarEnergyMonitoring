from accounts.models import User
from .models import Host
from rest_framework import permissions


class DoesRequestingUserExist(permissions.BasePermission):

    def has_permission(self, request, view):
        if User.objects.filter(id=request.user.id):
            return True
        return False


class IsLocationOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ('POST', 'PUT', 'DELETE'):
            return request.user.id == request.data['user']
        elif request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False
