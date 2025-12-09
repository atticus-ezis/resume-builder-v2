from django.urls import path
from .views import upload_pdf, confirm_context

urlpatterns = [
    path("upload/pdf/", upload_pdf, name="upload_pdf"),
    path("confirm/context/", confirm_context, name="confirm_context"),
]
