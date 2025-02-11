import random
from accounts.models import UserRegister,OTP
from django.utils import timezone
from datetime import timedelta


#otp generator
def otp_generator(email):
    user_instance = UserRegister.objects.get(email=email)
    otp = str(random.randint(1000,9999))
    obj = OTP(user=user_instance,otp=otp,expires_at= timezone.now() + timedelta(minutes=5))
    expiry_time= timezone.now() + timedelta(minutes=5)
    obj.save()  
    expiry_time += timedelta(hours=5, minutes=30)
    formatted_expiry_time = expiry_time.strftime("%Y-%m-%d %I:%M %p IST")
    return otp, formatted_expiry_time