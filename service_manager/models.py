from django.db import models
from service_manager.validators import validate_file_size  

class Service(models.Model):
    title = models.CharField(max_length=50, db_index=True)
    image = models.ImageField(upload_to='images_service/', null=True, blank=True, validators=[validate_file_size])  
    description = models.TextField()
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])

    def __str__(self):
        return self.title


class Subservice(models.Model):
    title = models.CharField(max_length=50, db_index=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='subservices')
    image = models.ImageField(upload_to='images_subservice/', null=True, blank=True, validators=[validate_file_size])  
    description = models.TextField()

    def __str__(self):
        return self.title
