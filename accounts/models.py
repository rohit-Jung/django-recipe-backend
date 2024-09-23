from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('chef', 'Chef'),
        ('meal_planner', 'Meal Planner'),
        ('food_enthusiast', 'Food Enthusiast')
        # Add more roles as needed
    )
    role = models.CharField(max_length=20, choices=ROLES, default='food_enthusiast')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    objects = CustomUserManager()  # Assign the custom manager

    def __str__(self):
        return self.username

    def get_profile_picture_url(self):
        if self.profile_picture:
            return f"{settings.BACKEND_URL}{self.profile_picture.url}"
        return None  # Default picture path
