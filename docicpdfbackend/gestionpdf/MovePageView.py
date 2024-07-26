from io import BytesIO

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from PyPDF2 import PdfReader, PdfWriter
from .models import PDF
from django.utils import timezone

class MovePageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pdf_id):
        page_number = request.data.get('page_number')
        new_position = request.data.get('new_position')

        if page_number is None or new_position is None:
            return Response({'error': 'page_number et new_position sont requis'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pdf = get_object_or_404(PDF, id=pdf_id)
            pdf_reader = PdfReader(pdf.file.path)
            pdf_writer = PdfWriter()

            pages = list(pdf_reader.pages)  # Convert to list to use pop and insert

            if page_number < 1 or page_number > len(pages) or new_position < 1 or new_position > len(pages):
                return Response({'error': 'Numéro de page ou nouvelle position invalide'}, status=status.HTTP_400_BAD_REQUEST)

            page = pages.pop(page_number - 1)
            pages.insert(new_position - 1, page)

            for page in pages:
                pdf_writer.add_page(page)

            output = BytesIO()
            pdf_writer.write(output)
            output.seek(0)

            original_file_name = pdf.file.name
            new_file_name = original_file_name.replace('.pdf', '') + '_movedpages.pdf'
            pdf.file.save(new_file_name, output)
            pdf.date_modification = timezone.now()
            pdf.save()

            return Response({'message': 'Page déplacée avec succès'}, status=status.HTTP_200_OK)
        except PDF.DoesNotExist:
            return Response({'error': 'PDF non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        except IndexError:
            return Response({'error': 'Index de page hors limites'}, status=status.HTTP_400_BAD_REQUEST)
