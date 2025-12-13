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
)
from ai_generation.models import JobApplication, Resume, CoverLetter
from ai_generation.services import APICall, UpdateContent, DownloadMarkdown
from rest_framework import status
# Create your views here.

# frontend must match context models


class GenerateResumeAndCoverLetterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_context, job_description, command = self.get_context(request)
        try:
            chat_response = APICall(user_context, job_description, command).execute()
            # Save drafts to database
            self.save_drafts(chat_response, job_description)
            return Response({"markdown": chat_response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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

    def save_drafts(self, responses, job_description):
        """Save generated content as drafts to Resume/CoverLetter models."""
        for response_dict in responses:
            for content_type, content in response_dict.items():
                if content_type == "resume":
                    Resume.objects.update_or_create(
                        user=self.request.user,
                        job_description=job_description,
                        defaults={"content": content},
                    )
                elif content_type == "cover letter":
                    CoverLetter.objects.update_or_create(
                        user=self.request.user,
                        job_description=job_description,
                        defaults={"content": content},
                    )


class UpdateContentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpdateContentSerializer(data=request.data)
        serializer.fields[
            "job_description_id"
        ].queryset = JobDescription.objects.filter(user=request.user)
        serializer.is_valid(raise_exception=True)
        content = serializer.validated_data["content"]
        instructions = serializer.validated_data["instructions"]
        content_type = serializer.validated_data["content_type"]
        job_description = serializer.validated_data["job_description"]
        try:
            chat_response = UpdateContent(content, instructions, content_type).execute()
            # Save draft to database
            self.save_draft(chat_response, job_description, content_type)
            return Response({"markdown": chat_response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def save_draft(self, markdown_content, job_description, content_type):
        """Save updated content as draft to Resume/CoverLetter models."""
        if content_type == "resume":
            Resume.objects.update_or_create(
                user=self.request.user,
                job_description=job_description,
                defaults={"content": markdown_content},
            )
        elif content_type == "cover letter":
            CoverLetter.objects.update_or_create(
                user=self.request.user,
                job_description=job_description,
                defaults={"content": markdown_content},
            )


class DownloadMarkdownView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file_name, job_description, content_type, markdown_content = self.get_context(
            request
        )

        # If markdown_content not provided, fetch from saved draft
        if not markdown_content:
            markdown_content = self.get_draft_content(job_description, content_type)
            if not markdown_content:
                return Response(
                    {
                        "message": f"No saved {content_type} found. Please generate or provide content."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

        # Generate PDF
        try:
            pdf_bytes = DownloadMarkdown(markdown_content, request).execute()
            response = HttpResponse(pdf_bytes, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{file_name}.pdf"'
        except Exception as e:
            return Response(
                {"message": f"Failed to generate PDF: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Update Resume/CoverLetter with final content (in case it was edited/overridden)
        resume_instance = None
        cover_letter_instance = None

        if content_type == "resume":
            resume_instance, _ = Resume.objects.update_or_create(
                user=request.user,
                job_description=job_description,
                defaults={"content": markdown_content},
            )
        elif content_type == "cover letter":
            cover_letter_instance, _ = CoverLetter.objects.update_or_create(
                user=request.user,
                job_description=job_description,
                defaults={"content": markdown_content},
            )

        # Create/update JobApplication with FK references to Resume/CoverLetter instances
        try:
            job_application, created = JobApplication.objects.get_or_create(
                user=request.user,
                job_description=job_description,
            )

            # Link Resume and CoverLetter instances to JobApplication
            if resume_instance:
                job_application.resume = resume_instance
            if cover_letter_instance:
                job_application.cover_letter = cover_letter_instance

            job_application.save()
        except Exception as e:
            return Response(
                {"message": f"Failed to save job application: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return response

    def get_context(self, request):
        serializer = DownloadMarkdownSerializer(data=request.data)
        serializer.fields[
            "job_description_id"
        ].queryset = JobDescription.objects.filter(user=request.user)
        serializer.is_valid(raise_exception=True)
        markdown_content = serializer.validated_data.get("markdown_content", "")
        file_name = serializer.validated_data["file_name"]
        job_description = serializer.validated_data["job_description"]
        content_type = serializer.validated_data["content_type"]
        return file_name, job_description, content_type, markdown_content

    def get_draft_content(self, job_description, content_type):
        """Fetch saved draft content from Resume/CoverLetter models."""
        try:
            if content_type == "resume":
                resume = Resume.objects.get(
                    user=self.request.user,
                    job_description=job_description,
                )
                return resume.content
            elif content_type == "cover letter":
                cover_letter = CoverLetter.objects.get(
                    user=self.request.user,
                    job_description=job_description,
                )
                return cover_letter.content
        except (Resume.DoesNotExist, CoverLetter.DoesNotExist):
            return None
        return None
