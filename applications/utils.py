from google import genai
from django.conf import settings
from pypdf import PdfReader

def extract_text_from_pdf(file_path):
    """Reads a PDF and returns the text inside it."""
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + " "
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text.strip()

def get_ai_match_score(resume_text, job_description):
    """Sends resume and job description to Google Gemini to get a match score."""
    
    # Set up the NEW Gemini client using your free .env key
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    # The prompt we send to Gemini
    prompt = f"""
    You are an expert Technical Recruiter. 
    Compare the following RESUME against the JOB DESCRIPTION.
    Give a match percentage from 0 to 100 based on skills, experience, and relevance.
    
    RESPOND WITH ONLY A SINGLE INTEGER (e.g., 85). DO NOT write sentences.
    
    RESUME:
    {resume_text[:2000]}
    
    JOB DESCRIPTION:
    {job_description}
    """

    try:
        # Use the new SDK syntax and the CORRECT model name from your list!
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        # Get the score from Gemini's reply
        score_str = response.text.strip()
        
        # Clean up the response just in case Gemini adds extra words
        score = int(''.join(filter(str.isdigit, score_str)))
        return min(max(score, 0), 100) # Ensure it's between 0 and 100
        
    except Exception as e:
        print(f"Gemini Error: {e}")
        return None