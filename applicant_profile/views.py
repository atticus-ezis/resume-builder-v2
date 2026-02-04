from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserContext
from .serializers import (
    FileUploadSerializer,
    UserContextListSerializer,
    UserContextSerializer,
)
from .services import PDFExtractor

# Create your views here.


class UserContextViewSet(viewsets.ModelViewSet):
    serializer_class = UserContextSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == "list":
            return UserContextListSerializer
        return UserContextSerializer

    def get_queryset(self):
        return UserContext.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_delete(self, serializer):
        serializer.delete(user=self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"], name="upload-pdf", url_path="upload-pdf")
    def upload_pdf(self, request):
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data["file"]
        name = serializer.validated_data["name"]

        pdf_extractor = PDFExtractor()
        text = pdf_extractor.execute(file)

        user_context = UserContext.objects.create(
            user=request.user,
            name=name,
            context=text,
        )
        return Response(
            {
                "message": "PDF file uploaded successfully",
                "id": user_context.id,
                "name": user_context.name,
                "updated_at": user_context.updated_at,
            },
            status=status.HTTP_200_OK,
        )
