from rest_framework.permissions import BasePermission
from accounts.models import UserRegister


class IsCustomer(BasePermission):
    
    def has_permission(self, request, view):
        try:
            user = UserRegister.objects.get(id=request.user.id)  
            print(user.name)
            return user.role == "customer" 
        except UserRegister.DoesNotExist:
            return False 
        
