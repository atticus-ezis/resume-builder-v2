from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from applicant_profile.models import UserContext
from job_profile.models import JobDescription
from ai_generation.serializers import MatchContextSerializer, UpdateContentSerializer
from ai_generation.services import APICall, UpdateContent
from rest_framework import status
# Create your views here.

# frontend must match context models


class GenerateResumeAndCoverLetterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_context, job_description, command = self.get_context(request)
        try:
            chat_response = APICall(user_context, job_description, command).execute()
            return Response({"response": chat_response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_context(self, request):
        # extract data
        serializer = MatchContextSerializer(data=request.data)

        serializer.fields["user_context_id"].queryset = self.get_queryset(
            UserContext.objects.filter(user=request.user)
        )
        serializer.fields["job_description_id"].queryset = self.get_queryset(
            JobDescription.objects.filter(user=request.user)
        )

        serializer.is_valid(raise_exception=True)

        user_context = serializer.validated_data["user_context"]
        job_description = serializer.validated_data["job_description"]

        command = serializer.validated_data["command"]

        return user_context, job_description, command


class UpdateContentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpdateContentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = serializer.validated_data["content"]
        instructions = serializer.validated_data["instructions"]
        content_type = serializer.validated_data["content_type"]
        try:
            chat_response = UpdateContent(content, instructions, content_type).execute()
            return Response({"response": chat_response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
