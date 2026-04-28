from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobs.models import Job
from .forms import ApplicationForm
from .models import Application
from .utils import extract_text_from_pdf, get_ai_match_score


@login_required(login_url='login')
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    if request.user.role != 'seeker':
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect('job_detail', slug=job.slug)
    
    if job.posted_by == request.user:
        messages.error(request, "You cannot apply to your own job posting.")
        return redirect('job_detail', slug=job.slug)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save() 
            
            # 1. Get the path of the uploaded PDF
            pdf_path = application.resume.path
            
            # 2. Read the text from the PDF
            resume_text = extract_text_from_pdf(pdf_path)
            
            # 3. If we found text, ask Google Gemini AI for a score
            if resume_text:
                job_description = f"{job.title} {job.description} {job.requirements}"
                score = get_ai_match_score(resume_text, job_description)
                
                # 4. Save the score to the database
                application.match_score = score
                application.save(update_fields=['match_score'])
                
            messages.success(request, "Your application has been submitted successfully!")
            return redirect('job_detail', slug=job.slug)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ApplicationForm()

    context = {
        'job': job,
        'form': form
    }
    return render(request, 'applications/apply.html', context)



@login_required
def candidate_dashboard(request):
    applications = Application.objects.filter(applicant=request.user).order_by('-applied_at')
    context = {'applications': applications}
    return render(request, 'applications/candidate_dashboard.html', context)

@login_required
def recruiter_dashboard(request):
    if request.user.role != 'recruiter':
        messages.error(request, "Access denied. Recruiters only.")
        return redirect('job_list')
    
    applications = Application.objects.filter(job__posted_by=request.user).order_by('-applied_at')
    context = {'applications': applications}
    return render(request, 'applications/recruiter_dashboard.html', context)

@login_required
def update_application_status(request, application_id, new_status):
    if request.user.role != 'recruiter':
        return redirect('job_list')
        
    application = get_object_or_404(Application, id=application_id, job__posted_by=request.user)
    
    valid_statuses = ['reviewed', 'shortlisted', 'accepted', 'rejected']
    if new_status in valid_statuses:
        application.status = new_status
        application.save()
        messages.success(request, f"Application status updated to {new_status}.")
    
    return redirect('recruiter_dashboard')