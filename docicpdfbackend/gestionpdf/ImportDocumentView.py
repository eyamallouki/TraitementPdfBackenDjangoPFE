from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import PDF
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import PDF
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO
from django.utils import timezone

class ImportDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pdf_id):
        document = request.FILES.get('document')
        if not document:
            return Response({'error': 'Aucun document fourni'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pdf = PDF.objects.get(id=pdf_id)
            pdf_reader = PdfReader(pdf.file.path)
            import_reader = PdfReader(document)
            pdf_writer = PdfWriter()

            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            for page in import_reader.pages:
                pdf_writer.add_page(page)

            output = BytesIO()
            pdf_writer.write(output)
            output.seek(0)

            original_file_name = pdf.file.name
            new_file_name = original_file_name.replace('.pdf', '') + '_imported.pdf'
            pdf.file.save(new_file_name, output)
            pdf.total_pages += len(import_reader.pages)
            pdf.date_modification = timezone.now()
            pdf.save()

            return Response({'message': 'Document importé avec succès'}, status=status.HTTP_200_OK)
        except PDF.DoesNotExist:
            return Response({'error': 'PDF non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)