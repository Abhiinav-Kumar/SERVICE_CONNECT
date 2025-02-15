from django.contrib import admin
from service_manager.models import Service,Subservice,ServiceRegistry,ServiceRequest,Review
# Register your models here.

admin.site.register(Service)
admin.site.register(Subservice)
admin.site.register(ServiceRegistry)
admin.site.register(ServiceRequest)
admin.site.register(Review)
