import PyPDF2
from rest_framework import status


class PDFExtractor:
    def execute(self, pdf_file):
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        except Exception as e:
            raise e

        if text == "":
            return "No text found in PDF file", status.HTTP_400_BAD_REQUEST
        return text
