from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    creator = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE, null=False, blank=False)
    tags = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.title



