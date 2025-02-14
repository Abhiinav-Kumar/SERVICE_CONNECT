from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from accounts.models import UserRegister,OTP,Profile
from accounts.api.serializers import UsersSerializer,RegisterSerializer,LoginSerializer,OTPSerializer,ProfileSerializer,ProfileViewSerializer

from django.utils import timezone

from accounts.utils import otp_generator

from django.conf import settings
from django.core.mail import send_mail

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated




#Users list view
class UsersListAV(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        users = UserRegister.objects.all()
        serializer = UsersSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    
#users registering view
class RegisterUsersAV(APIView):
    
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data,"message":"Account Created Successfully"},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)
        
        
      
#login view  
class LoginUserAV(APIView):
    
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = UserRegister.objects.get(email=email)
            except UserRegister.DoesNotExist:
                return Response({"error": "Invalid Email id"}, status=status.HTTP_401_UNAUTHORIZED)
            if check_password(password, user.password):
                
                otp,expiry_time = otp_generator(email)
                
                # email setup
                subject = "Your One-Time Password (OTP) for Secure Login"
                message = f"Dear {user.name},\n\nWe received a request to log in to your account. Please use the following One-Time Password (OTP) to proceed: \n🔒 OTP: {otp} \nThis OTP is valid for 5 minutes and will expire at {expiry_time}. and should not be shared with anyone for security reasons.\nIf you did not request this OTP, please ignore this email.\n\nBest regards,\nSERVICE CONNECT "

                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]
                
                try:
                    send_mail(subject, message, from_email, recipient_list)
                    return Response({"message": "Login successful. OTP sent to your email."}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"error": "Failed to send OTP email", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            

#OTP verify View
class VerifyOtpAV(APIView):
    
    def post(self,request):
        serializer = OTPSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            
            try:
                user = UserRegister.objects.get(email=email)
                latest_otp_record = OTP.objects.filter(user=user).order_by('-created_at').first()
            
                if not latest_otp_record:
                    return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

                if latest_otp_record.expires_at < timezone.now():  
                    return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
                
                if latest_otp_record.otp == otp:
                    OTP.objects.filter(user=user).delete()
                    
                    #token generating
                    refresh = RefreshToken.for_user(user)
                    return Response({"message": "OTP verified successfully", "access": str(refresh.access_token),"refresh": str(refresh)}, status=status.HTTP_200_OK)
                
                return Response({"error": "Incorrect OTP"}, status=status.HTTP_400_BAD_REQUEST)
            
            except UserRegister.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

#profile View
class ProfileAV(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        try:
            user = Profile.objects.get(user=request.user)
            serializer = ProfileViewSerializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "Profile Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        
    
    def post(self,request):
        serializer = ProfileSerializer(data=request.data)
        
        if Profile.objects.filter(user=request.user).exists():
            return Response({"error": "Profile Already Created"},status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"data":serializer.data,"message": "Profile Created"},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        
    
    def put(self,request):
        try:
            profile = Profile.objects.get(user=request.user)  
        except Profile.DoesNotExist:
            return Response({"error": "Profile Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data,"message":"Successfully Updated"},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)
        
        
    def delete(self,request):
        try:
            profile = Profile.objects.get(user=request.user)  
        except Profile.DoesNotExist:
            return Response({"error": "Profile Not Found"}, status=status.HTTP_404_NOT_FOUND)
        profile.delete()
        return Response({"message":"Successfully Deleted"},status=status.HTTP_204_NO_CONTENT)



class LogoutViewAV(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":"Invalid token"},status=status.HTTP_400_BAD_REQUEST)
        
        
    
    
    
    