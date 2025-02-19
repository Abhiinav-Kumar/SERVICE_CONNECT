from rest_framework import serializers
from service_manager.models import ServiceRequest,Service,Subservice,Review
from django.db.models import Avg



class ServiceRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ServiceRequest
        fields = "__all__"
        
        
class ReviewRatingSerializers(serializers.ModelSerializer):
    user = serializers.CharField(source="user.name")
    service = serializers.CharField(source="service.title")
    service_provider = serializers.CharField(source="service_provider.name")
    
    class Meta:
        model = Review
        fields = ['user','service','service_provider','rating','comment']
        
        


# Search serializer
class ReviewSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source='user.name', read_only=True)
    # service_provider = serializers.CharField(source='service_provider.name', read_only=True)
    class Meta:
        model = Review
        fields = ['rating']      
        
        
class SubserviceSerializer(serializers.ModelSerializer):
    
    # review_set = ReviewSerializer(many=True,read_only = True)
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Subservice
        fields = ["title",'rating'] 
        
    def get_rating(self, obj):
        avg_rating = obj.review_set.aggregate(Avg('rating'))['rating__avg']  
        return round(avg_rating, 1) if avg_rating is not None else "Be the first to give a rating"
    
    
class ServiceSerializer(serializers.ModelSerializer):
    
    subservices = SubserviceSerializer(many=True,read_only = True)
    
    class Meta:
        model = Service
        fields = ["title","subservices"] 
        
