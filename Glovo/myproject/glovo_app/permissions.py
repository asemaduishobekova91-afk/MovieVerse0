from rest_framework.permissions import BasePermission


class CheckRolePermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'client'

class CheckCourierPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'courier'

class CreateStorePermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'owner'