from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    """ This class manage all posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username}"
