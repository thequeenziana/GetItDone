
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, default='default_profile_pic/default.jpg')
    bio = models.TextField(blank=True)
    interests = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
