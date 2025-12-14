from django.db import models
from django.contrib.auth.models import User


# User Context Model
class UserContext(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes")
    name = models.CharField(max_length=255)
    context = models.JSONField(required=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
