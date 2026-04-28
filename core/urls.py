from django.contrib import admin
from django.urls import path, include
from users.views import register_web_view, login_web_view, logout_web_view
from core import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Your Existing APIs
    path('api/auth/', include('users.urls')), 
    path('api/companies/', include('companies.urls')),
    path('api/jobs/', include('jobs.urls')),
    
    # HTML Web Auth Routes (Changed names here!)
    path('register/', register_web_view, name='register'),
    path('login/', login_web_view, name='login'),
    path('logout/', logout_web_view, name='logout'),
    
    # HTML Dashboards & Applications
    path('', include('applications.urls')),
      path('', include('jobs.urls')), 
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)