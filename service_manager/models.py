from django.db import models
from service_manager.validators import validate_file_size  
from accounts.models import EmployeeRegistration,UserRegister

class Service(models.Model):
    title       = models.CharField(max_length=50, db_index=True)
    image       = models.ImageField(upload_to='images_service/', null=True, blank=True, validators=[validate_file_size])  
    description = models.TextField()
    status      = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])

    def __str__(self):
        return self.title


class Subservice(models.Model):
    title       = models.CharField(max_length=50, db_index=True)
    service     = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='subservices')
    image       = models.ImageField(upload_to='images_subservice/', null=True, blank=True, validators=[validate_file_size])  
    description = models.TextField()

    def __str__(self):
        return self.title
    
class ServiceRegistry(models.Model):
    employee       = models.ForeignKey(EmployeeRegistration, on_delete=models.CASCADE)
    service_name  = models.ForeignKey(Service, on_delete=models.CASCADE)  
    subservice_name  = models.ForeignKey(Subservice, on_delete=models.CASCADE,null=True, blank=True)  
    min_price     = models.PositiveIntegerField()
    max_price     = models.PositiveIntegerField()
    description   = models.TextField()

    def __str__(self):
        return f" - {self.service_name.title} - {self.subservice_name.title}"


class ServiceRequest(models.Model):
    service_registry = models.ForeignKey(ServiceRegistry, on_delete=models.CASCADE)
    customer = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployeeRegistration, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField() 
    end_time = models.DateTimeField()   
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.customer}"
    

class Review(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)  
    service = models.ForeignKey(Subservice, on_delete=models.CASCADE,related_name='review_set')  
    service_provider = models.ForeignKey(EmployeeRegistration,on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  
    comment = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return f"{self.user.name} - {self.service}-{self.service_provider} - {self.rating}/5"