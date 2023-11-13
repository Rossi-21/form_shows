from django.db import models
from django.contrib.auth.models import User

class Show(models.Model):
    title = models.CharField(max_length=256)
    network = models.CharField(max_length=256)
    release_date = models.DateField()
    description = models.TextField()
    created_at =  models.DateTimeField(auto_now_add=True, null = True)
    updated_at = models.DateTimeField(auto_now=True, null= True)
