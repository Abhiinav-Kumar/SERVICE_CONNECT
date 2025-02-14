from rest_framework.permissions import BasePermission
from accounts.models import UserRegister

class IsCustomer(BasePermission):
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            user = UserRegister.objects.get(id=request.user.id)
            return user.role == "customer"
        except UserRegister.DoesNotExist:
            return False