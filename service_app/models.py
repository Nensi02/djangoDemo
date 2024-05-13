from django.db import models

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