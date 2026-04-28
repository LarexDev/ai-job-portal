from django.db import models
from django.utils.text import slugify

class Company(models.Model):
    # 1-to-1 relationship: One Recruiter owns ONE Company
    owner = models.OneToOneField(
        'users.CustomUser', 
        on_delete=models.CASCADE, 
        related_name='company',
        limit_choices_to={'role': 'recruiter'} # Extra security at DB level
    )
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    website = models.URLField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    employee_count = models.CharField(max_length=50, blank=True, help_text="e.g., 50-100")
    location = models.CharField(max_length=200, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-generate slug from company name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name