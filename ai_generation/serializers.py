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
    document_version_id = serializers.PrimaryKeyRelatedField(
        queryset=DocumentVersion.objects.none(),
        source="document_version",
        required=False,
        allow_null=True,
    )
    instructions = serializers.CharField(required=True)
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if obj.markdown:
            return obj.markdown
        else:
            return obj.document_version.markdown

    def validate(self, val):
        markdown = val.get("markdown")
        document_version = val.get("document_version")

        if markdown is not None and document_version is not None:
            raise serializers.ValidationError(
                "Either 'markdown' or 'document_version_id' must be provided, but not both."
            )

        if markdown is None and document_version is None:
            raise serializers.ValidationError(
                "Either 'markdown' or 'document_version_id' must be provided."
            )

        return val


class DocumentVersionResponseSerializer(serializers.ModelSerializer):
    """Serializer for DocumentVersion response format used across multiple views."""

    document = serializers.SerializerMethodField()
    document_version = serializers.SerializerMethodField()

    class Meta:
        model = DocumentVersion
        fields = ["markdown", "document", "document_version"]

    def get_document(self, obj):
        return {
            "id": obj.document.id,
            "type": obj.document.document_type,
        }

    def get_document_version(self, obj):
        return {
            "id": obj.id,
            "version": obj.version_number,
        }


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
