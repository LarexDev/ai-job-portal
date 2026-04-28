import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import UserManager 

# The choices we defined
ROLE_CHOICES = (
    ('seeker', 'Job Seeker'),
    ('recruiter', 'Recruiter'),
)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='seeker')
    
    # Security Flags
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Django System Flags (Comes from PermissionsMixin, but good to declare defaults)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False) 
    
    # Audit Trails
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Connect our custom manager
    objects = UserManager()

    # Tell Django to use EMAIL to login, not username
    USERNAME_FIELD = 'email'
    
    # Required when typing `python manage.py createsuperuser`
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email

# --- ADD THIS BELOW YOUR CUSTOMUSER CLASS ---

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SeekerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='seeker_profile')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200, blank=True, help_text="e.g., Senior Python Developer")
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    bio = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name='seekers')
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.email}'s Seeker Profile"


class RecruiterProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='recruiter_profile')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    designation = models.CharField(max_length=150, blank=True, help_text="e.g., HR Manager")
    is_company_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}'s Recruiter Profile"