from django.urls import path
from .views import CompanyCreateView

urlpatterns = [
    path('create/', CompanyCreateView.as_view(), name='create-company'),
]