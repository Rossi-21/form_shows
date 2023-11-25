from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE )
    description = models.TextField()

class Show(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    network = models.CharField(max_length=256)
    release_date = models.DateField()
    description = models.TextField()
    show_image = models.ImageField(null=True, blank=True, upload_to="images/")
    like = models.ManyToManyField(User, related_name='liked_shows', blank=True)
    comment = models.ManyToManyField(Comment, related_name='commented_shows', blank=True)
    created_at =  models.DateTimeField(auto_now_add=True, null = True)
    updated_at = models.DateTimeField(auto_now=True, null= True)


