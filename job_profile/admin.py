from django.contrib import admin

from .models import JobDescription


@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "company_name",
        "job_position",
        "user",
        "created_at",
        "updated_at",
    )
    list_filter = ("user",)
    search_fields = ("company_name", "job_position", "user__email")
    raw_id_fields = ("user",)
    ordering = ("user", "-created_at")
