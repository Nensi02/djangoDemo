from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    access_token = models.CharField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)  # For email verification

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        # Generate a new access token when saving the user instance
        super().save(*args, **kwargs)

# Create your models here.
class Services(models.Model):
    status_value = [
        (1, 'active'),
        (0, 'inactive')
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=True)
    description = models.TextField(null=True)
    status = models.BooleanField(choices=status_value, default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name