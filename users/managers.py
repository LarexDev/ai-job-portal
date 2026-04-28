from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # 1. Email is mandatory
        if not email:
            raise ValueError('Users must have an email address')
        
        # 2. Normalize email (convert to lowercase)
        email = self.normalize_email(email)
        
        # 3. Create the user model instance
        user = self.model(email=email, **extra_fields)
        
        # 4. Hash the password using Django's built-in security
        user.set_password(password)
        
        # 5. Save to MySQL database
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # 1. Force these flags for the root admin
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('role', 'seeker') # Superadmin base role

        # 2. Safety check: If someone passes is_staff=False, raise error
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # 3. Reuse the create_user logic we wrote above
        return self.create_user(email, password, **extra_fields)