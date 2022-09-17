from django.db import models
from django.contrib.auth.models import User
from post.models import Post

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favourite = models.ManyToManyField(Post, blank=True)
    
    def __str__(self):
        return f'{self.user}' '-Profile'