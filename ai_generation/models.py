from django.db import models
from django.contrib.auth.models import User
from job_profile.models import JobDescription

# Create your models here.


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes")
    job_description = models.ForeignKey(
        JobDescription, on_delete=models.CASCADE, related_name="resumes"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "job_description")

    def __str__(self):
        return f"{self.user.username} - {self.job_description.company_name} Resume"


class CoverLetter(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cover_letters"
    )
    job_description = models.ForeignKey(
        JobDescription, on_delete=models.CASCADE, related_name="cover_letters"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "job_description")

    def __str__(self):
        return (
            f"{self.user.username} - {self.job_description.company_name} Cover Letter"
        )


class JobApplication(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="job_applications"
    )
    job_description = models.ForeignKey(
        JobDescription, on_delete=models.CASCADE, related_name="job_applications"
    )
    resume = models.ForeignKey(
        Resume,
        on_delete=models.SET_NULL,
        related_name="job_applications",
        null=True,
        blank=True,
    )
    cover_letter = models.ForeignKey(
        CoverLetter,
        on_delete=models.SET_NULL,
        related_name="job_applications",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "job_description")

    def __str__(self):
        return f"{self.user.username} - {self.job_description.company_name}"
