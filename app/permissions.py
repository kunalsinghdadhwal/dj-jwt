"""
Task Tracker Custom Permissions

This module defines custom permission classes for task ownership.
"""

from rest_framework import permissions


class IsTaskOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a task to access it.

    - Safe methods (GET, HEAD, OPTIONS) are allowed only if the user owns the task.
    - Unsafe methods (POST, PUT, PATCH, DELETE) are allowed only if the user owns the task.
    """

    message = 'You do not have permission to access this task.'

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is the owner of the task.

        Args:
            request: The HTTP request
            view: The view being accessed
            obj: The task object

        Returns:
            bool: True if user owns the task, False otherwise
        """
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.

    Read permissions are allowed to any authenticated user,
    but write permissions are only allowed to the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check permissions based on request method.

        Args:
            request: The HTTP request
            view: The view being accessed
            obj: The object being accessed

        Returns:
            bool: True if permission granted, False otherwise
        """
        # Read permissions for safe methods
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user

        # Write permissions only for owner
        return obj.user == request.user
