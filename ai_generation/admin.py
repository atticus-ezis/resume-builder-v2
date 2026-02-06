from django.contrib import admin

from .models import Document, DocumentVersion


class DocumentVersionInline(admin.TabularInline):
    model = DocumentVersion
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "document_type",
        "job_description",
        "user_context",
        "created_at",
    )
    list_filter = ("document_type", "user")
    search_fields = ("document_type", "user__email")
    raw_id_fields = ("user", "user_context", "job_description", "final_version")
    inlines = [DocumentVersionInline]
    ordering = ("user", "-created_at")


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ("id", "document", "created_at", "version_name")
    list_filter = ("document__document_type", "document__user")
    search_fields = ("document__user__email", "version_name")
    raw_id_fields = ("document",)
    ordering = ("document__user", "-created_at")
