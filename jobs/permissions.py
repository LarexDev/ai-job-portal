from rest_framework import permissions

class IsCompanyOwner(permissions.BasePermission):
    """
    Allows access only to recruiters who have an active company profile.
    """
    def has_permission(self, request, view):
        is_recruiter = request.user.is_authenticated and request.user.role == 'recruiter'
        
        # hasattr prevents a 500 error if they are a recruiter but haven't made a company yet
        has_company = hasattr(request.user, 'company')
        
        return bool(is_recruiter and has_company)