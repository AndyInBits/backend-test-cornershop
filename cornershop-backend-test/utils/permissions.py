# Django Rest Framework
from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Allows access only to manager users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_manager)
