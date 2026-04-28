from django.db import models
from django.utils.text import slugify

JOB_TYPE_CHOICES = (
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
    ('contract', 'Contract'),
    ('internship', 'Internship'),
    ('remote', 'Remote'),
)

JOB_STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('closed', 'Closed'),
    ('expired', 'Expired'),
)

class Job(models.Model):
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    
    posted_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='posted_jobs',
        limit_choices_to={'role': 'recruiter'}
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    status = models.CharField(max_length=20, choices=JOB_STATUS_CHOICES, default='draft')
    
    experience_min = models.PositiveIntegerField(default=0, help_text="In years")
    experience_max = models.PositiveIntegerField(null=True, blank=True, help_text="In years")
    
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_salary_disclosed = models.BooleanField(default=False)
    
    vacancy_count = models.PositiveIntegerField(default=1)
    is_featured = models.BooleanField(default=False)
    
    deadline = models.DateTimeField(null=True, blank=True)
    
    skills = models.ManyToManyField('users.Skill', blank=True, related_name='jobs')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} at {self.company.name}"