from django.urls import path
from .views import RegisterView, register_web_view, login_web_view, logout_web_view

urlpatterns = [
    # Your existing API route
    path('register/', RegisterView.as_view(), name='api_register'),
   
    # New HTML Web routes
    path('web/register/', register_web_view, name='register_web'),
    path('web/login/', login_web_view, name='login_web'),
    path('web/logout/', logout_web_view, name='logout_web'),
]