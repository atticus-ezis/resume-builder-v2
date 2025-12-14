from job_profile.models import JobDescription
from job_profile.serializers import (
    JobDescriptionSerializer,
    JobDescriptionListSerializer,
)
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class JobDescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = JobDescriptionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == "list":
            return JobDescriptionListSerializer
        return JobDescriptionSerializer

    def get_queryset(self):
        return JobDescription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        job_context = serializer.validated_data["job_context"]
        job_position = job_context.get("job_position")
        serializer.save(user=self.request.user, job_position=job_position)

    def perform_update(self, serializer):
        job_context = serializer.validated_data["job_context"]
        job_position = job_context.get("job_position")
        serializer.save(user=self.request.user, job_position=job_position)

    def perform_delete(self, serializer):
        serializer.delete(user=self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
