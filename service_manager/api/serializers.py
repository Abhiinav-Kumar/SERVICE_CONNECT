from rest_framework import serializers
from service_manager.models import ServiceRequest

class ServiceRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ServiceRequest
        fields = "__all__"
        