from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):  # type: ignore
        if request.user and request.user.is_authenticated:
            return request.user.groups.filter(name="Doctor").exists()

        return False
