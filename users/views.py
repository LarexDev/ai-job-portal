from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser      # <-- ADD THIS LINE
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        # Override create to send a custom JSON response instead of just 201 Created
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            "success": True,
            "message": "User registered successfully. Please verify your email.",
            "data": {
                "email": user.email,
                "role": user.role
            }
        }, status=status.HTTP_201_CREATED)
    
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm # Make sure you created this forms.py earlier!

def register_web_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            if user.role == 'recruiter':
                return redirect('recruiter_dashboard')
            return redirect('candidate_dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_web_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            
            # ---> ADD THIS NEW LOGIC <---
            # 1. Check if there is a 'next' parameter (e.g., ?next=/job/some-job/)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # 2. If no 'next' parameter, do the normal role-based redirect
            if user.role == 'recruiter':
                return redirect('recruiter_dashboard')
            return redirect('candidate_dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            
    return render(request, 'users/login.html')

def logout_web_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login_web')
