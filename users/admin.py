from django.contrib import admin
from .models import CustomUser, Skill, SeekerProfile, RecruiterProfile

admin.site.register(CustomUser)
admin.site.register(Skill)
admin.site.register(SeekerProfile)
admin.site.register(RecruiterProfile)