from django.db import models
from django.core.validators import FileExtensionValidator

APPLICATION_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('reviewed', 'Reviewed'),
    ('shortlisted', 'Shortlisted'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
)

class Application(models.Model):
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='applications')
    
    cover_letter = models.TextField(blank=True)
    
    resume = models.FileField(
        upload_to='applicant_resumes/', 
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
        help_text="Upload your resume (PDF, DOC, DOCX)"
    )
    
    # AI Match Score Field
    match_score = models.IntegerField(null=True, blank=True, help_text="AI Match Percentage (0-100)")
    
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Prevents a user from applying to the same job twice
        unique_together = ('job', 'applicant') 

    def __str__(self):
        return f"{self.applicant.email} applied for {self.job.title}"