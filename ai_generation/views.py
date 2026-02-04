from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ai_generation.models import Document, DocumentVersion
from ai_generation.serializers import (
    DocumentListSerializer,
    DocumentSerializer,
    DocumentVersionResponseSerializer,
    DocumentVersionSerializer,
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

# Create your views here.

# frontend must match context models


class GenerateResumeAndCoverLetterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pretend_response = [
            {
                "markdown": "test resume hello world",
                "document": {"id": 1, "type": "resume"},
                "document_version": {"id": 1, "version": 1},
            },
            {
                "markdown": "test cover letter hello mrs hiring manager",
                "document": {"id": 2, "type": "cover_letter"},
                "document_version": {"id": 2, "version": 1},
            },
        ]
        return Response(pretend_response, status=status.HTTP_200_OK)

        user_context, job_description, commands = self.get_context(request)
        response_data = []
        for command in commands:
            generate_new_version = True
            # command can be both
            document, document_created = Document.objects.get_or_create(
                user=request.user,
                user_context=user_context,
                job_description=job_description,
                document_type=command,
            )
            if not document_created:
                existing_document_version = (
                    document.final_version
                    or document.versions.order_by("created_at").last()
                )
                if existing_document_version:
                    document_version = existing_document_version
                    generate_new_version = False

            if generate_new_version:
                try:
                    chat_responses = APICall(
                        user_context, job_description, command
                    ).execute()
                except Exception as e:
                    return Response(
                        {"detail": "AI Request Failed", "message": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                for response in chat_responses:
                    command = response["command"]
                    markdown = response["markdown"]
                    document_version = DocumentVersion.objects.create(
                        document=document,
                        markdown=markdown,
                    )
            serializer = DocumentVersionResponseSerializer(document_version)
            response_data.append(serializer.data)
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

        user_context = serializer.validated_data["user_context"]
        job_description = serializer.validated_data["job_description"]
        commands = serializer.validated_data["command"]

        return user_context, job_description, commands


class UpdateContentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpdateContentSerializer(data=request.data)
        serializer.fields[
            "document_version_id"
        ].queryset = DocumentVersion.objects.filter(document__user=request.user)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get("return_old"):
            document_version = serializer.validated_data.get("return_old")
        else:
            document_version = serializer.validated_data["document_version"]
            markdown = (
                serializer.validated_data.get("markdown") or document_version.markdown
            )
            instructions = serializer.validated_data.get("instructions") or None
            version_name = serializer.validated_data.get("version_name") or None

            document = document_version.document
            document_type = document.document_type

            try:
                if instructions:
                    markdown_response = UpdateContent(
                        markdown, instructions, document_type, version_name
                    ).execute()
                else:
                    markdown_response = markdown
                create_kwargs = {
                    "document": document,
                    "markdown": markdown_response,
                }
                if version_name:
                    create_kwargs["version_name"] = version_name
                document_version = DocumentVersion.objects.create(**create_kwargs)
                serializer = DocumentVersionResponseSerializer(document_version)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


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


class DocumentVersionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = DocumentVersionSerializer

    def get_queryset(self):
        queryset = DocumentVersion.objects.filter(
            document__user=self.request.user
        ).select_related("document")

        # Filter by document_id if provided
        document_id = self.request.query_params.get("document", None)
        if document_id:
            queryset = queryset.filter(document_id=document_id)

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
