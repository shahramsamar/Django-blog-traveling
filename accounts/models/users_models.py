from django.db import models
from django.contrib.auth.models import(
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    """custom user manager"""
    
    def create_user(self,email,password, **extra_fields):
        """ create user and save it """
        if not email:
            raise ValueError(("The email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    
    def create_superuser(self,email,password,**extra_fields):
        """ create and save superuser """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_verified',True)
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is _superuser=true')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must have is_stuff=true')
        
        return self.create_user(email, password,**extra_fields)
         
class User(AbstractBaseUser,PermissionsMixin):
    """ this user  for our application"""  
    email = models.EmailField(max_length=100,unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)     
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    def __str__(self):
        return self.email