from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class UserManager(BaseUserManager):
    
    def create_user(self,email,name,password=None,phone_number=None,role="customer"):
        if not email:
            raise ValueError("Users must have an email address")
        if not name:
            raise ValueError("Users must have a name")
        
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            phone_number = phone_number,
            role = role,
        )
        user.set_password(password)
    
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,name,password=None): 
        user = self.create_user(
            email = self.normalize_email(email),
            name = name,
            password = password,
            role = 'admin'
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser  = True
        
        user.save(using=self._db)
        return user

class UserRegister(AbstractBaseUser):
    name         = models.CharField(max_length=50)
    email        = models.EmailField(max_length=100,unique=True)
    # password   = models.CharField(max_length=20)
    phone_number = models.BigIntegerField(null=True,blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    role         = models.CharField(max_length=50,default='customer')
    
    is_active    = models.BooleanField(default=True)
    is_admin     = models.BooleanField(default=False)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    
class OTP(models.Model):
    user       = models.ForeignKey(UserRegister,on_delete=models.CASCADE)
    otp        = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    


class Profile(models.Model):
    user            = models.ForeignKey(UserRegister,on_delete=models.CASCADE)
    full_name       = models.CharField(max_length=50)
    address         = models.TextField()
    date_of_birth   = models.DateField()
    gender          = models.CharField(max_length=20)
    house_name      = models.CharField(max_length=20)
    land_mark       = models.CharField(max_length=20)
    pincode         = models.CharField(max_length=20)
    district        = models.CharField(max_length=20)
    state           = models.CharField(max_length=20)
    created_at      = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.full_name