from django.contrib import admin
from accounts.models import UserRegister,OTP,Profile,EmployeeRegistration

# Register your models here.
admin.site.register(UserRegister)
admin.site.register(OTP)
admin.site.register(Profile)
admin.site.register(EmployeeRegistration)