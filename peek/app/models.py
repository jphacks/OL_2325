from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser,PermissionsMixin)
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=1000)
    img = models.ImageField(upload_to="", blank=False, null=False)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    favorite_count = models.IntegerField(default=0)
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comment")
    body = models.TextField(max_length=1000, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.body
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_favorite")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_favorite")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + " likes " + self.post.title
    

