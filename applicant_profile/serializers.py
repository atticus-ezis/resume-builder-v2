from rest_framework import serializers
from .models import UserContext


class UserContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContext
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith(".pdf"):
            raise serializers.ValidationError("File must be a PDF")
        return value
