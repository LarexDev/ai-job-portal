from django import forms
from .models import Job

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        # We exclude company, posted_by, slug, and status because we will set those automatically in the view!
        exclude = ['company', 'posted_by', 'slug', 'status', 'created_at', 'updated_at']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add basic CSS classes to make it look clean
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})