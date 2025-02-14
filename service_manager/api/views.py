from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from service_manager.api.serializers import ServiceRequestSerializer
from service_manager.models import ServiceRequest
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

class ServiceBookingAV(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
    
        data = ServiceRequest.objects.filter(customer=request.user.id)
        print(request.user.id)
        if not data.exists():
            return Response({"message": "No Booking"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ServiceRequestSerializer(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = ServiceRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data,"message":"Booking Successfully"},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)
        
    def put(self,request,booking_id):
        try:
            data = ServiceRequest.objects.get(id=booking_id,customer=request.user.id)  
        except ServiceRequest.DoesNotExist:
            return Response({"error": "Data Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ServiceRequestSerializer(data,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data,"message":"Successfully Updated Booking"},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,booking_id):
        try:
            booking = ServiceRequest.objects.get(id=booking_id,customer=request.user.id)  
        except ServiceRequest.DoesNotExist:
            return Response({"error": "Data Not Found"}, status=status.HTTP_404_NOT_FOUND)
        booking.delete()
        return Response({"message": "Booking Successfully Deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    