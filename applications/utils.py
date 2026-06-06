from google import genai
from django.conf import settings
from pypdf import PdfReader

def extract_text_from_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + " "
    except Exception as e:
        print(f"PDF READ ERROR: {e}")
    return text.strip()

def get_ai_match_score(resume_text, job_description):
    print("=== AI SCORING STARTED ===")
    print(f"Resume length: {len(resume_text)}")
    
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        prompt = f"""
        Compare the RESUME against the JOB DESCRIPTION.
        Give a match percentage from 0 to 100.
        RESPOND WITH ONLY A SINGLE INTEGER (e.g., 85). DO NOT write sentences.
        
        RESUME:
        {resume_text[:2000]}
        
        JOB DESCRIPTION:
        {job_description}
        """

        print("Sending to Gemini...")
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        
        # Force print the raw response
        raw_text = response.text
        print(f"RAW GEMINI TEXT: {repr(raw_text)}")
        
        # Clean up the response
        score_str = raw_text.strip()
        
        # Extract ONLY numbers from the string
        numbers = ''.join(filter(str.isdigit, score_str))
        print(f"EXTRACTED NUMBERS: {numbers}")
        
        if numbers:
            score = int(numbers)
            score = min(max(score, 0), 100)
            print(f"FINAL SCORE CALCULATED: {score}")
            return score
        else:
            print("ERROR: No numbers found in Gemini response!")
            return 0
            
    except Exception as e:
        print(f"!!! CRITICAL GEMINI ERROR: {e} !!!")
        return 0