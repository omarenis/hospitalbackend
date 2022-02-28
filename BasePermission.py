from rest_framework.permissions import BasePermissionMetaclass


class BasePermission(metaclass=BasePermissionMetaclass):

    def has_permission(self, request, view):
        print(view)
        return True
