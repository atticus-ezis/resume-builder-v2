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
        choices=["generate_resume", "generate_cover_letter", "generate_both"],
    )


class UpdateContentSerializer(serializers.Serializer):
    markdown = serializers.CharField(required=False, allow_null=True)
    document_version_id = serializers.PrimaryKeyRelatedField(
        queryset=DocumentVersion.objects.none(),
        source="document_version",
        required=True,
    )
    instructions = serializers.CharField(required=True)

    def validate(self, val):
        return create_new_version_if_needed(val)


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
    file_name = serializers.CharField(required=True)
    markdown = serializers.CharField(required=False, allow_blank=True)
    document_version_id = serializers.PrimaryKeyRelatedField(
        queryset=DocumentVersion.objects.none(),
        source="document_version",
        required=True,
    )

    def validate(self, val):
        return create_new_version_if_needed(val)


def create_new_version_if_needed(val):
    document_version = val.get("document_version")
    markdown = val.get("markdown")
    document = document_version.document

    if not markdown or markdown.strip() == "":
        return val

    if document_version.markdown.strip() != markdown.strip():
        create_new_document_version = DocumentVersion.objects.create(
            document=document,
            markdown=markdown,
        )
        document_version = create_new_document_version

        val["document_version"] = document_version

    return val


class DocumentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    draft_count = serializers.SerializerMethodField()

    def get_content(self, obj):
        if obj.final_version:
            return obj.final_version.markdown
        return None

    def get_drafts(self, obj):
        return obj.versions.count()

    class Meta:
        model = Document
        fields = [
            "id",
            "job_description",
            "user_context",
            "document_type",
            "content",
            "draft_count",
            "created_at",
        ]


class DocumentListSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    job_position = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ["id", "document_type", "company_name", "job_position"]

    def get_company_name(self, obj):
        return obj.job_description.company_name

    def get_job_position(self, obj):
        return obj.job_description.job_position


class DocumentVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentVersion
        fields = ["id", "document", "version_number", "markdown", "created_at"]
        read_only_fields = ["id", "version_number", "created_at"]
