from django.contrib import admin
from accounts.models import UserRegister,OTP,Profile

# Register your models here.
admin.site.register(UserRegister)
admin.site.register(OTP)
admin.site.register(Profile)