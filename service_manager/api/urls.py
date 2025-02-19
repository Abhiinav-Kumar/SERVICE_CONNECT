from django.urls import path
from service_manager.api.views import ServiceBookingAV,AllServiceAV,ReviewRatingAV


urlpatterns = [
    path('servicebooking/',ServiceBookingAV.as_view(),name="serviceBooking"),
    path('servicebooking/<int:booking_id>/',ServiceBookingAV.as_view(),name="serviceBooking"),
    path('allservice/',AllServiceAV.as_view(),name="allservice"),
    path('rating/',ReviewRatingAV.as_view(),name="rating"),
    
    
]
