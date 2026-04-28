from django.urls import path
from .views import JobCreateView
from . import views

urlpatterns = [
    path('create/', JobCreateView.as_view(), name='create-job'),
    path('post/', views.post_job, name='post_job'),
    path('', views.job_list, name='job_list'), # This will be our homepage!
    path('job/<slug:slug>/', views.job_detail, name='job_detail'),
]