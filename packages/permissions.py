from rest_framework import permissions


class IsAdminOrIssuedBy(permissions.BasePermission):
    """
    Allows access to admin users or the employee who issued the package.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.issued_by == request.user