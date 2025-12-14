from rest_framework import serializers
from applicant_profile.models import UserContext
from job_profile.models import JobDescription
from ai_generation.models import DocumentVersion, Document


class MatchContextSerializer(serializers.Serializer):
    user_context_id = serializers.PrimaryKeyRelatedField(
        queryset=UserContext.objects.none(), source="user_context"
    )
    job_description_id = serializers.PrimaryKeyRelatedField(
        queryset=JobDescription.objects.none(), source="job_description"
    )
    command = serializers.ChoiceField(
        required=True,
        multiple_choices=["generate_resume", "generate_cover_letter", "generate_both"],
    )


class UpdateContentSerializer(serializers.Serializer):
    markdown = serializers.CharField(required=False, allow_null=True)
    instructions = serializers.CharField(required=True)
    document_version_id = serializers.PrimaryKeyRelatedField(
        queryset=DocumentVersion.objects.none(), source="document_version"
    )
    document = serializers.SerializerMethodField()
    document_version = serializers.SerializerMethodField()

    def get_document(self, obj):
        document = obj.document_version.document
        data = {}
        data["id"] = document.id
        data["document_type"] = document.document_type
        return data

    def get_document_version(self, obj):
        data = {}
        data["id"] = obj.document_version.id
        data["version_number"] = obj.document_version.version_number
        return data

    class Meta:
        fields = ["markdown", "instructions", "document_version_id"]
        read_only_fields = ["markdown", "document", "document_version"]


class DownloadMarkdownSerializer(serializers.Serializer):
    markdown_content = serializers.CharField(required=False, allow_blank=True)
    file_name = serializers.CharField(required=True)
    job_description_id = serializers.PrimaryKeyRelatedField(
        queryset=JobDescription.objects.none(), source="job_description"
    )
    content_type = serializers.ChoiceField(
        required=True,
        choices=["resume", "cover letter"],
    )
