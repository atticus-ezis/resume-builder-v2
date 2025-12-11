from rest_framework import serializers
from .models import JobDescription


class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = ["id", "company_name", "job_context", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class JobDescriptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = ["id", "company_name", "created_at", "updated_at"]
        read_only_fields = "__all__"
