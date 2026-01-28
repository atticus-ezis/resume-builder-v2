from django.db import models
from django.contrib.auth.models import User


# Job Description Model
class JobDescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    company_name = models.CharField(max_length=255)
    job_position = models.CharField(max_length=255)
    job_context = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} - {self.job_position}"
