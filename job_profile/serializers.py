from rest_framework import serializers
from .models import JobDescription


class JobDescriptionSerializer(serializers.ModelSerializer):
    def validate_job_context(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("job_context must be a JSON object")
        needed_fields = [
            "job_position",
            "company_name",
            "company_overview",
            "job_description",
            "job_requirements",
        ]
        missing_fields = []
        for field in needed_fields:
            if field not in value:
                missing_fields.append(field)
        if missing_fields:
            raise serializers.ValidationError(f"Fields {missing_fields} are required")
        return value

    class Meta:
        model = JobDescription
        fields = [
            "id",
            "company_name",
            "job_context",
            "job_position",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class JobDescriptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = ["id", "company_name", "job_position", "updated_at"]
        read_only_fields = ["id", "company_name", "job_position", "updated_at"]
