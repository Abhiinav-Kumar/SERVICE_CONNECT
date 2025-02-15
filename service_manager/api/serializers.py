from rest_framework import serializers
from service_manager.models import ServiceRequest,Service,Subservice

class ServiceRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ServiceRequest
        fields = "__all__"
        

# Search serializer      
        
class SubserviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subservice
        fields = ["title"] 
        
class ServiceSerializer(serializers.ModelSerializer):
    
    subservices = SubserviceSerializer(many=True,read_only = True)
    
    class Meta:
        model = Service
        fields = ["title","subservices"] 
        
