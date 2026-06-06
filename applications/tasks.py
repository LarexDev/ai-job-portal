from celery import shared_task
from django.core.files.storage import default_storage
from .utils import extract_text_from_pdf, get_ai_match_score
from .models import Application

@shared_task
def calculate_ai_match_score(application_id):
    """
    This runs in the background! 
    It takes the application ID, gets the file, reads it, 
    asks AI for a score, and saves it to the database.
    """
    try:
        # Fetch the application from the database
        application = Application.objects.get(id=application_id)
        
        # Open the PDF from storage
        file_path = application.resume.path
        resume_text = extract_text_from_pdf(file_path)
        
        if resume_text:
            job_description = f"{application.job.title} {application.job.description} {application.job.requirements}"
            score = get_ai_match_score(resume_text, job_description)
            
            # Save the score back to the database!
            application.match_score = score
            application.save(update_fields=['match_score'])
            
    except Exception as e:
        print(f"Celery Task Error: {e}")