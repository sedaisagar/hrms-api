from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from utils.generators import generate_client_id, generate_employee_id
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
    
    client_id = models.CharField(max_length=50, default=generate_client_id)
    address = models.TextField()

    social_links = models.JSONField(default=dict)

    class Meta:
        db_table = "client_profile"

class Department(CommonModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        db_table = "department"

class Designation(CommonModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        db_table = "designation"

class Teams(CommonModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="teams")

    class Meta:
        db_table = "teams"

class EmployeeProfile(CommonModel):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'), 
    ]
    EMPLOYMENT_STATUS_CHOICES = [
        ('employed', 'Employed'),
        ('unemployed', 'Unemployed'),
        ('self-employed', 'Self-Employed'),
        ('student', 'Student'),
        ('retired', 'Retired'),
    ]
    MARITIAL_STATUS = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile")
    team = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True, blank=True, related_name="employee_profile")
    reports_to = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="subordinates")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="employee_profile")
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True, related_name="employee_profile") 

    employee_id = models.CharField(max_length=50, default=generate_employee_id)

    full_name = models.CharField(max_length=100)
    years_of_experience = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    gender = models.CharField(max_length=20, blank=True, null=True, choices=GENDER_CHOICES)
    bith_date = models.DateField(blank=True, null=True)
    address = models.TextField()

    # Personal Information
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    passport_expiry_date = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    maritial_status = models.CharField(max_length=20, blank=True, null=True, choices=MARITIAL_STATUS)
    employment_of_spouse = models.CharField(max_length=20, blank=True, null=True, choices=EMPLOYMENT_STATUS_CHOICES)
    number_of_children = models.PositiveIntegerField(blank=True, null=True)

    about = models.TextField(blank=True, null=True)

    # Educational Qualifications
    institution_name = models.CharField(max_length=100, blank=True, null=True)
    course = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    # Previous Employment Details
    previous_company_name = models.CharField(max_length=100, blank=True, null=True)
    previous_designation = models.CharField(max_length=100, blank=True, null=True)
    previous_start_date = models.DateField(blank=True, null=True)
    previous_end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "employee_profile"


class EmergencyContact(CommonModel):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="emergency_contacts")
    
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)

    phone_number = models.CharField(max_length=15)
    alt_phone_number = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = "emergency_contact"

