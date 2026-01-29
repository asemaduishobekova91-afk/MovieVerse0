from rest_framework import permissions


class CheckSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'seller':
            return True
        return False


class CheckBuyer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'buyer':
            return True
        return False
