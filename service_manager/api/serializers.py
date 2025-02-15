from rest_framework import serializers
from service_manager.models import ServiceRequest,Service,Subservice,Review

class ServiceRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ServiceRequest
        fields = "__all__"
        

# Search serializer
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = Review
        fields = ['user','service_provider','rating']      
        
        
class SubserviceSerializer(serializers.ModelSerializer):
    
    review_set = ReviewSerializer(many=True,read_only = True)
    
    class Meta:
        model = Subservice
        fields = ["title",'review_set'] 
        
class ServiceSerializer(serializers.ModelSerializer):
    
    subservices = SubserviceSerializer(many=True,read_only = True)
    
    class Meta:
        model = Service
        fields = ["title","subservices"] 
        
