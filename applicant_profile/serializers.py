from django.db import IntegrityError
from rest_framework import serializers

from .models import UserContext, compute_context_hash


def _integrity_error_to_validation_error(exc):
    """Convert DB IntegrityError to ValidationError with a clear message."""
    message = str(exc)
    if "unique_name_per_user" in message:
        raise serializers.ValidationError(
            {"name": "You already have a context with this name."}
        )
    if "unique_context_per_user" in message:
        raise serializers.ValidationError("A context with this content already exists.")
    raise serializers.ValidationError(
        "A context with this name or content already exists for your account."
    )


class UserContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContext
        fields = ["id", "name", "context", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        if not request or not request.user:
            return attrs

        user = request.user
        name = attrs.get("name")
        context = attrs.get("context")

        qs = UserContext.objects.filter(user=user)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if name is not None and qs.filter(name=name).exists():
            raise serializers.ValidationError(
                {"name": "You already have a context with this name."}
            )
        if context is not None:
            context_hash = compute_context_hash(context)
            if qs.filter(context_hash=context_hash).exists():
                raise serializers.ValidationError(
                    "A context with this content already exists."
                )
        return attrs

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            _integrity_error_to_validation_error(e)

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError as e:
            _integrity_error_to_validation_error(e)


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
