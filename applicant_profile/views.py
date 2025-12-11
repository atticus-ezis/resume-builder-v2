from rest_framework.response import Response
from rest_framework import status
from .services import PDFExtractor
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserContextSerializer,
    FileUploadSerializer,
    UserContextListSerializer,
)
from rest_framework import viewsets
from .models import UserContext
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action


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

    @action(detail=False, methods=["post"], name="upload-pdf")
    def upload_pdf(self, request):
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pdf_extractor = PDFExtractor()
        text = pdf_extractor.execute(serializer.validated_data["file"])
        return Response(
            {"message": "PDF file uploaded successfully", "text": text},
            status=status.HTTP_200_OK,
        )
