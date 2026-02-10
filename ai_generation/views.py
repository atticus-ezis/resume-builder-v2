from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ai_generation.constants import COMMAND_TO_DOCUMENT_TYPES
from ai_generation.models import Document, DocumentVersion
from ai_generation.serializers import (
    DocumentListSerializer,
    DocumentSerializer,
    DocumentVersionHistoryResponseSerializer,
    DocumentVersionResponseSerializer,
    MatchContextSerializer,
    UpdateContentSerializer,
)
from ai_generation.services import (  # noqa: F401
    APICall,
    DownloadMarkdown,
    UpdateContent,
)
from applicant_profile.models import UserContext
from job_profile.models import JobDescription
from resume_builder.utils import compute_context_hash

# Create your views here.

# frontend must match context models


class GenerateResumeAndCoverLetterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # pretend_response = [
        #     {
        #         "markdown": "test resume hello world",
        #         "document": {"id": 1, "type": "resume"},
        #         "document_version": {"id": 1, "version": 1},
        #     },
        #     {
        #         "markdown": "test cover letter hello mrs hiring manager",
        #         "document": {"id": 2, "type": "cover_letter"},
        #         "document_version": {"id": 2, "version": 1},
        #     },
        # ]
        # return Response(pretend_response, status=status.HTTP_200_OK)

        request_data = self.get_context(request)
        regenerate_version = request_data.get("regenerate_version", False)
        commands = COMMAND_TO_DOCUMENT_TYPES[request_data["command"]]
        response_data = []
        for command in commands:
            message = ""
            document, _ = Document.objects.get_or_create(
                user=request.user,
                user_context=request_data["user_context"],
                job_description=request_data["job_description"],
                document_type=command,
            )

            document_version = None
            if not regenerate_version:
                existing = (
                    document.final_version
                    or document.versions.order_by("-updated_at").first()
                )
                if existing and existing.markdown:
                    document_version = existing
                    message = "returned existing document"

            if document_version is None:
                try:
                    chat_responses = APICall(
                        request_data["user_context"],
                        request_data["job_description"],
                        command,
                    ).execute()
                except Exception as e:
                    return Response(
                        {"detail": "AI Request Failed", "message": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                context_hash = compute_context_hash(chat_responses)
                document_version, _ = DocumentVersion.objects.get_or_create(
                    document=document,
                    context_hash=context_hash,
                    defaults={"markdown": chat_responses},
                )
                message = "returned regenerated document"

            serializer = DocumentVersionResponseSerializer(document_version)
            item = {"document_version": serializer.data}
            if message:
                item["message"] = message
            response_data.append(item)
        return Response(response_data, status=status.HTTP_200_OK)

    def get_context(self, request):
        # extract data
        serializer = MatchContextSerializer(data=request.data)

        serializer.fields["user_context_id"].queryset = UserContext.objects.filter(
            user=request.user
        )
        serializer.fields[
            "job_description_id"
        ].queryset = JobDescription.objects.filter(user=request.user)

        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


class UpdateContentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpdateContentSerializer(data=request.data)
        serializer.fields[
            "document_version_id"
        ].queryset = DocumentVersion.objects.filter(document__user=request.user)
        serializer.is_valid(raise_exception=True)
        document_version = serializer.validated_data["document_version"]
        instructions = serializer.validated_data["instructions"]

        try:
            markdown_response = UpdateContent(instructions, document_version).execute()
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        document_version.patch(markdown=markdown_response)
        document_version.save()
        serializer = DocumentVersionResponseSerializer(document_version)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return DocumentListSerializer
        return DocumentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DocumentVersionHistory(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentVersionHistoryResponseSerializer
    ordering = ["-updated_at"]

    def get_queryset(self):
        queryset = DocumentVersion.objects.filter(
            document__user=self.request.user
        ).select_related("document")
        document_id = self.request.query_params.get("document")
        if document_id:
            queryset = queryset.filter(document_id=document_id)
        return queryset


class DocumentVersionViewSet(viewsets.ModelViewSet):
    """
    List/retrieve document versions. Filter by document: ?document=<document_id>
    When document is specified, uses DocumentVersionResponseSerializer.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = DocumentVersionResponseSerializer
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = DocumentVersion.objects.filter(
            document__user=self.request.user
        ).select_related("document")
        # document_id = self.request.query_params.get("document")
        # if document_id:
        #     queryset = queryset.filter(document_id=document_id)
        return queryset

    @action(detail=True, methods=["get"], name="pdf_download", url_path="pdf")
    def pdf_download(self, request, pk=None):
        document_version = get_object_or_404(DocumentVersion, id=pk)
        markdown = document_version.markdown
        file_name = document_version.version_name

        try:
            pdf_bytes = DownloadMarkdown(markdown, request).execute()
            response = HttpResponse(pdf_bytes, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{file_name}.pdf"'
            return response
        except Exception as e:
            return Response(
                {"message": f"Failed to generate PDF: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
