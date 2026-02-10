from django.db import IntegrityError
from rest_framework import serializers

from ai_generation.constants import COMMAND_CHOICES, COMMAND_TO_DOCUMENT_TYPES
from ai_generation.models import Document, DocumentVersion
from applicant_profile.models import UserContext
from job_profile.models import JobDescription


class MatchContextSerializer(serializers.Serializer):
    user_context_id = serializers.PrimaryKeyRelatedField(
        queryset=UserContext.objects.none(), source="user_context", required=True
    )
    job_description_id = serializers.PrimaryKeyRelatedField(
        queryset=JobDescription.objects.none(), source="job_description", required=True
    )
    command = serializers.ChoiceField(choices=COMMAND_CHOICES, required=True)

    commands = serializers.SerializerMethodField()

    def get_commands(self, obj):
        command = obj.get("command")
        if command in COMMAND_CHOICES:
            commands = COMMAND_TO_DOCUMENT_TYPES[command]
        else:
            raise serializers.ValidationError(
                "Invalid command, must select from: generate_resume, generate_cover_letter, generate_both"
            )
        return commands


class UpdateContentSerializer(serializers.Serializer):
    document_version_id = serializers.PrimaryKeyRelatedField(
        queryset=DocumentVersion.objects.none(),
        source="document_version",
        required=True,
    )
    instructions = serializers.CharField(required=False, allow_null=True)

    def validate(self, val):
        if not val.get("instructions"):
            raise serializers.ValidationError("New instructions, must be provided")

        return val


class DocumentVersionHistoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentVersion
        fields = ["id", "version_name", "updated_at"]
        read_only_fields = ["id", "updated_at", "version_name"]


class DocumentVersionResponseSerializer(serializers.ModelSerializer):
    """Serializer for DocumentVersion response format used across multiple views."""

    document = serializers.SerializerMethodField()

    class Meta:
        model = DocumentVersion
        fields = ["id", "markdown", "document", "version_name", "updated_at"]
        read_only_fields = ["id", "document", "updated_at"]

    def get_document(self, obj):
        return {
            "id": obj.document.id,
            "type": obj.document.document_type,
        }

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            return handle_integrity_error(e)


class DocumentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    draft_count = serializers.SerializerMethodField()

    def get_content(self, obj):
        if obj.final_version:
            return obj.final_version.markdown
        return None

    def get_drafts(self, obj):
        return obj.versions.count()

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            return handle_integrity_error(e)

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


# class DocumentVersionSerializer(serializers.ModelSerializer):
#     document_type = serializers.SerializerMethodField()

#     def get_document_type(self, obj):
#         return obj.document.document_type

#     class Meta:
#         model = DocumentVersion
#         fields = [
#             "id",
#             "document",
#             "version_name",
#             "markdown",
#             "created_at",
#             "document_type",
#         ]
#         read_only_fields = ["id", "version_name", "created_at", "document_type"]


def handle_integrity_error(exc):
    msg = str(exc)
    if "unique_name_per_document" in msg:
        raise serializers.ValidationError(
            "A version with this name already exists for this document"
        )
    if "unique_markdown_per_document" in msg:
        raise serializers.ValidationError(
            "A version with this markdown already exists for this document"
        )
    if "unique_document_type_per_user_context_and_job_description" in msg:
        raise serializers.ValidationError(
            "A document with this type already exists for this user, job description and personal info"
        )
    raise serializers.ValidationError(msg)
