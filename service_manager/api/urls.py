from django.urls import path
from service_manager.api.views import ServiceBookingAV


urlpatterns = [
    path('serviceBooking/',ServiceBookingAV.as_view(),name="serviceBooking"),
    path('serviceBooking/<int:booking_id>/',ServiceBookingAV.as_view(),name="serviceBooking"),
]
