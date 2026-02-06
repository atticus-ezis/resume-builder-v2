from django.contrib import admin

from .models import UserContext


@admin.register(UserContext)
class UserContextAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "created_at", "updated_at")
    list_filter = ("user",)
    search_fields = ("name", "context_hash", "user__email")
    raw_id_fields = ("user",)
    ordering = ("user", "-created_at")
