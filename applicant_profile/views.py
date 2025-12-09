from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .services import PDFExtractor
from rest_framework.permissions import IsAuthenticated
from .models import UserContext

# Create your views here.


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_pdf(request):
    resume_pdf = request.FILES.get("pdf_file")
    if resume_pdf:
        pdf_extractor = PDFExtractor()
        text = pdf_extractor.execute(resume_pdf)

        return Response(
            {"message": "PDF file uploaded successfully", "text": text},
            status=status.HTTP_200_OK,
        )
    return Response(
        {"message": "No PDF file uploaded. Check file name is 'resume_pdf'"},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_context(request):
    context = request.data.get("context")
    name = request.data.get("name")

    if not context or not name:
        return Response(
            {"message": "No context or name uploaded."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = request.user
    UserContext.objects.create(
        user=user,
        context=context,
        name=name,
    )
    return Response(
        {"message": "PDF file confirmed successfully"},
        status=status.HTTP_200_OK,
    )
