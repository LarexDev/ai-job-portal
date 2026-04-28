from rest_framework import permissions

class IsRecruiter(permissions.BasePermission):
    """
    Only allows access to users with role='recruiter'.
    """
    def has_permission(self, request, view):
        # Must be authenticated, must be a recruiter, and must have verified email
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'recruiter' and
            request.user.is_verified
        )