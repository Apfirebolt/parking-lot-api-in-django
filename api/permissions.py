from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    message = 'Only a superuser is allowed to perform this action'

    # for object level permissions
    def has_permission(self, request, view):
        return request.user.is_superuser



