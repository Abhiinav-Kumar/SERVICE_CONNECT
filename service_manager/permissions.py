from rest_framework.permissions import BasePermission
from accounts.models import UserRegister

import logging

logger = logging.getLogger(__name__)

class IsCustomer(BasePermission):
    
    def has_permission(self, request, view):
        
        logger.info(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")

        # Ensure user is authenticated
        if not request.user or not request.user.is_authenticated:
            logger.warning("Access denied: User is not authenticated")
            return False
        
        # Ensure user has a role and it is 'customer'
        user_role = getattr(request.user, 'role', None)
        logger.info(f"User Role: {user_role}")

        if user_role != "customer":
            logger.warning("Access denied: User is not a customer")
            return False
        
        return True
