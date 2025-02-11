from rest_framework import serializers
from accounts.models import UserRegister,Profile

class UsersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserRegister
        fields = "__all__"
        

class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserRegister
        fields = ['name','email','phone_number','password',]
        extra_kwargs = {'password': {'write_only': True}} 
        
    def create(self, validated_data):
        return UserRegister.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number')
        )
        
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    
class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)
    
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ["user"]
        
        
class ProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        
