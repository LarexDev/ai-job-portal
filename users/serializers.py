from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    # These fields are only for INPUT. They will NOT be saved to MySQL.
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'role', 'password', 'password_confirmation')

    def validate(self, attrs):
        # 1. Check if passwords match
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        # 2. Check password strength (Basic interview check)
        if len(attrs['password']) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters."})

        # 3. Remove password_confirmation so it doesn't try to save to MySQL
        attrs.pop('password_confirmation')
        return attrs

    def create(self, validated_data):
        # Call the UserManager we created earlier!
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number'),
            role=validated_data.get('role', 'seeker')
        )
        return user