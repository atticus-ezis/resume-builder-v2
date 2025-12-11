from rest_framework import serializers
from applicant_profile.models import UserContext
from job_profile.models import JobDescription


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
    content = serializers.CharField(required=True)
    instructions = serializers.CharField(required=True)
    content_type = serializers.ChoiceField(
        required=True,
        choices=["resume", "cover letter"],
    )
