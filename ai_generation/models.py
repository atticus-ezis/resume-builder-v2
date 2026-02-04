from django.contrib.auth.models import User
from django.db import models

from applicant_profile.models import UserContext
from job_profile.models import JobDescription

# Create your models here.


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    user_context = models.ForeignKey(
        UserContext, on_delete=models.CASCADE, related_name="documents"
    )
    job_description = models.ForeignKey(
        JobDescription, on_delete=models.CASCADE, related_name="documents"
    )
    document_type = models.CharField(
        max_length=255, choices=[("resume", "Resume"), ("cover_letter", "Cover Letter")]
    )
    final_version = models.ForeignKey(
        "DocumentVersion",  # forward reference
        on_delete=models.SET_NULL,
        related_name="final_version",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_description.company_name} - {self.document_type}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "user_context", "job_description", "document_type"],
                name="unique_job_per_user",
            )
        ]


class DocumentVersion(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="versions"
    )
    markdown = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    version_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Version {self.id} of {self.document.job_description.company_name} - {self.document.document_type} - {self.created_at}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.version_name:
            existing_versions = self.document.versions.count()
            if existing_versions > 0:
                self.version_name = f"{str(self.document)} - {existing_versions + 1}"
            else:
                self.version_name = f"{str(self.document)} - 1"
        super().save(*args, **kwargs)
