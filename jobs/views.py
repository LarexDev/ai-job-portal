from .forms import JobPostForm
from rest_framework import generics
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job
from .serializers import JobSerializer
from .permissions import IsCompanyOwner

# --- YOUR EXISTING API VIEW ---
class JobCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsCompanyOwner]

    def perform_create(self, serializer):
        # SECURELY attach the recruiter's company to the job
        serializer.save(company=self.request.user.company)

# --- NEW HTML VIEWS ---
def job_list(request):
    jobs = Job.objects.filter(status='published').order_by('-created_at')
    context = {'jobs': jobs}
    return render(request, 'jobs/job_list.html', context)

def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug, status='published')
    context = {'job': job}
    return render(request, 'jobs/job_detail.html', context)

@login_required
def post_job(request):
    # Only recruiters can post jobs
    if request.user.role != 'recruiter':
        messages.error(request, "Only recruiters can post jobs.")
        return redirect('job_list')
    
    # Ensure the recruiter actually created a Company profile first
    if not hasattr(request.user, 'company'):
        messages.error(request, "Please create a Company profile before posting a job.")
        return redirect('recruiter_dashboard')

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            # Save but don't commit to DB yet
            job = form.save(commit=False)
            # Attach the company and the user securely behind the scenes
            job.company = request.user.company
            job.posted_by = request.user
            job.status = 'published' # Automatically publish it
            job.save()
            # Save the many-to-many skills field
            form.save_m2m() 
            
            messages.success(request, "Job posted successfully!")
            return redirect('job_list')
    else:
        form = JobPostForm()

    context = {'form': form}
    return render(request, 'jobs/post_job.html', context)