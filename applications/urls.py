from django.urls import path
from . import views

urlpatterns = [
    path('job/<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),
    
    # Dashboard URLs
    path('dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('recruiter/dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    
    # Status update URL (e.g., /applications/5/update/rejected/)
    path('<int:application_id>/update/<str:new_status>/', views.update_application_status, name='update_application_status'),
]