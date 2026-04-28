from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, SeekerProfile, RecruiterProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    # 'created' is True ONLY when a brand new row is inserted into MySQL
    if created:
        if instance.role == 'seeker':
            SeekerProfile.objects.create(user=instance)
        elif instance.role == 'recruiter':
            RecruiterProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    # This ensures the profile saves whenever the user saves
    if instance.role == 'seeker' and hasattr(instance, 'seeker_profile'):
        instance.seeker_profile.save()
    elif instance.role == 'recruiter' and hasattr(instance, 'recruiter_profile'):
        instance.recruiter_profile.save()