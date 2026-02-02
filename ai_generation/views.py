from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from applicant_profile.models import UserContext
from job_profile.models import JobDescription
from ai_generation.serializers import (
    MatchContextSerializer,
    UpdateContentSerializer,
    DownloadMarkdownSerializer,
    DocumentVersionResponseSerializer,
    DocumentListSerializer,
    DocumentSerializer,
    DocumentVersionSerializer,
)
from ai_generation.models import Document, DocumentVersion
from ai_generation.services import APICall, UpdateContent, DownloadMarkdown
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
# Create your views here.

# frontend must match context models


class GenerateResumeAndCoverLetterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_context, job_description, command = self.get_context(request)
        try:
            chat_responses = APICall(user_context, job_description, command).execute()
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        pretend_response = [
            {
                "markdown": "test resume hello world",
                "document": {"id": 1, "type": "resume"},
                "document_version": {"id": 1, "version": 1},
            },
            {
                "markdown": "test cover letter hello mrs hiring manager",
                "document": {"id": 1, "type": "cover_letter"},
                "document_version": {"id": 1, "version": 1},
            },
        ]
        return Response(pretend_response, status=status.HTTP_200_OK)
        # try:
        #     responses = []
        #     for response in chat_responses:
        #         command = response["command"]
        #         markdown = response["markdown"]
        #         document, _ = Document.objects.get_or_create(
        #             user=request.user,
        #             user_context=user_context,
        #             job_description=job_description,
        #             document_type=command,
        #         )
        #         document_version = DocumentVersion.objects.create(
        #             document=document,
        #             markdown=markdown,
        #         )
        #         serializer = DocumentVersionResponseSerializer(document_version)
        #         responses.append(serializer.data)
        #     return Response(responses, status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response(
        #         {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )

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
        command = serializer.validated_data["command"]

        return user_context, job_description, command


class UpdateContentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpdateContentSerializer(data=request.data)
        serializer.fields[
            "document_version_id"
        ].queryset = DocumentVersion.objects.filter(document__user=request.user)
        serializer.is_valid(raise_exception=True)

        document_version = serializer.validated_data["document_version"]
        markdown = (
            serializer.validated_data.get("markdown") or document_version.markdown
        )
        instructions = serializer.validated_data.get("instructions") or None

        document = document_version.document
        document_type = document.document_type

        try:
            if instructions:
                markdown_response = UpdateContent(
                    markdown, instructions, document_type
                ).execute()
            else:
                # No instructions → use provided markdown (serializer ensures it's present)
                markdown_response = markdown
            document_version = DocumentVersion.objects.create(
                document=document,
                markdown=markdown_response,
            )
            serializer = DocumentVersionResponseSerializer(document_version)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DownloadMarkdownView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file_name, document_version = self.get_context(request)
        # Generate PDF
        try:
            markdown = document_version.markdown
            pdf_bytes = DownloadMarkdown(markdown, request).execute()
            response = HttpResponse(pdf_bytes, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{file_name}.pdf"'
            # finalize the DocumentVersion
            document = document_version.document
            document.final_version = document_version
            document.save()
            return response
        except Exception as e:
            return Response(
                {"message": f"Failed to generate PDF: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_context(self, request):
        serializer = DownloadMarkdownSerializer(data=request.data)
        serializer.fields[
            "document_version_id"
        ].queryset = DocumentVersion.objects.filter(document__user=request.user)
        serializer.is_valid(raise_exception=True)
        document_version = serializer.validated_data["document_version"]
        file_name = serializer.validated_data["file_name"]

        return file_name, document_version


# Document Management


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
