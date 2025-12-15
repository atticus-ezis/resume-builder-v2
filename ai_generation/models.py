from django.db import models
from django.contrib.auth.models import User
from job_profile.models import JobDescription
from applicant_profile.models import UserContext

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
    version_number = models.IntegerField(default=1)

    def __str__(self):
        return f"Version {self.id} of {self.document.job_description.company_name} - {self.document.document_type} - {self.created_at}"

    def save(self, *args, **kwargs):
        if not self.pk:
            last = (
                DocumentVersion.objects.filter(document=self.document)
                .order_by("-version_number")
                .first()
            )
            if last:
                self.version_number = last.version_number + 1
        super().save(*args, **kwargs)
