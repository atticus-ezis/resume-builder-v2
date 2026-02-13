from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework import serializers


class CustomRegisterSerializer(RegisterSerializer):
    username = None

    def get_cleaned_data(self):
        return {
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    email_verified = serializers.SerializerMethodField()
    application_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "email_verified",
            "application_count",
            "date_joined",
        ]

    def get_application_count(self, obj):
        return obj.documents.values("job_description_id").distinct().count()

    def get_email_verified(self, obj):
        return obj.emailaddress_set.filter(verified=True).exists()
