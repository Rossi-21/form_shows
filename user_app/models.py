from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Profile Model extends Django User Model with profile image and follows
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
# When User Profile is created, the User will automaticly follow themselves
def create_profile(sender, instance, created, **kwargs):
    # If a Profile is created
    if created: 
        # Create a variable with the Profile that was just made
        user_profile = Profile(user=instance)
        # Save the Profile to the database
        user_profile.save()
        # Set the Profile to follow itself
        user_profile.follows.set([instance.profile.id])
        # Save the Profile to the database
        user_profile.save()
# connect the profile to the User
post_save.connect(create_profile, sender=User)

#Comment Model
class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE )
    description = models.TextField()

# Show model
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


