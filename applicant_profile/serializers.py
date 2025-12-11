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
        read_only_fields = "__all__"


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith(".pdf"):
            raise serializers.ValidationError("File must be a PDF")
        return value
