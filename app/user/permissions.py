"""Permissions for users in all of views this project."""

import logging
from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)


class IsSuperuser(BasePermission):
    """Permissions for superusers."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
    

class IsStaff(BasePermission):
    """Permissions for staffs."""

    def has_permission(self, request, view):
        has_permission = request.user.is_authenticated and request.user.is_staff
        logger.debug(f"User {request.user.email} is_staff: {request.user.is_staff}, has_permission: {has_permission}")
        return has_permission
        # return request.user.is_authenticated and request.user.is_staff
    

class IsCoach(BasePermission):
    """Permissions for coaches"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_coach
    

class IsJudge(BasePermission):
    """Permissions for judges"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_judge
    

class IsObserver(BasePermission):
    """Permissions for observers"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_observer
