from job_profile.models import JobDescription
from job_profile.serializers import JobDescriptionSerializer
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated


class JobDescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = JobDescriptionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return JobDescription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
