from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    updated_at = models.DateTimeField(auto_now=True, null= True)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    if created: 
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)

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


