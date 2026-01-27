from rest_framework import serializers
from .models import UserContext


class UserContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContext
        fields = ["id", "name", "context", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class UserContextListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContext
        fields = ["id", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "name", "created_at", "updated_at"]


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    name = serializers.CharField(required=True)

    def validate_file(self, value):
        if value.content_type != "application/pdf":
            raise serializers.ValidationError("File must be a PDF")

        if not value.name.endswith(".pdf"):
            raise serializers.ValidationError("File must be a PDF")

        max_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_size:
            raise serializers.ValidationError("File must be less than 10MB")

        file_signature = value.read(4)
        value.seek(0)

        if file_signature != b"%PDF":
            raise serializers.ValidationError("Invalid PDF file format")

        return value
