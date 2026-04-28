from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    # This tells DRF to read the owner's email, but NOT accept it during creation
    owner_email = serializers.EmailField(source='owner.email', read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'slug', 'logo', 'website', 'description', 
                  'industry', 'employee_count', 'location', 'is_verified', 'owner_email')
        read_only_fields = ('id', 'slug', 'is_verified', 'owner_email') # User cannot set these