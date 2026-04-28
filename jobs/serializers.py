from rest_framework import serializers
from django.utils import timezone
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    # Read-only fields to show data nicely, but prevent user manipulation
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = Job
        fields = '__all__' # For speed in this project, we expose all fields
        read_only_fields = ('id', 'slug', 'company', 'company_name', 'created_at', 'updated_at')

    def validate(self, attrs):
        # RULE 1: Salary logic
        salary_min = attrs.get('salary_min')
        salary_max = attrs.get('salary_max')
        
        if salary_min and salary_max and salary_min > salary_max:
            raise serializers.ValidationError({
                "salary_max": "Maximum salary cannot be less than minimum salary."
            })
            
        # RULE 2: Deadline logic
        deadline = attrs.get('deadline')
        if deadline and deadline <= timezone.now():
            raise serializers.ValidationError({
                "deadline": "Deadline must be a future date."
            })
            
        # RULE 3: Experience logic
        exp_min = attrs.get('experience_min', 0)
        exp_max = attrs.get('experience_max')
        if exp_max is not None and exp_min > exp_max:
            raise serializers.ValidationError({
                "experience_max": "Max experience cannot be less than min experience."
            })

        return attrs