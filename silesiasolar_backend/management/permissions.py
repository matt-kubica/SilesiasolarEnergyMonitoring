from django.contrib.auth.models import User
from rest_framework import permissions


class DoesRequestingUserExist(permissions.BasePermission):

    def has_permission(self, request, view):
        if User.objects.filter(id=request.user.id):
            return True
        return False


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.id == request.data['user']

