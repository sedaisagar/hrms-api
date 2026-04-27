from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from utils.models import CommonModel
# Create your models here.

class CustomUserManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields["role"] = "admin"
        return super().create_superuser(username, email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'), # Client
        ('employee', 'Employee'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)

    objects = CustomUserManager()

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    

class ClientProfile(CommonModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")

    full_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    
    client_id = models.CharField(max_length=50)
    address = models.TextField()

    social_links = models.JSONField(default=dict)

    class Meta:
        db_table = "client_profile"


