from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import PDF
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO
from django.utils import timezone

class ExtractPagesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pdf_id):
        pages_to_extract = request.data.get('pages_to_extract', [])
        if not pages_to_extract:
            return Response({'error': 'Aucune page spécifiée pour extraction'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pdf = get_object_or_404(PDF, id=pdf_id)
            pdf_reader = PdfReader(pdf.file.path)
            pdf_writer = PdfWriter()

            for page_num in pages_to_extract:
                if page_num < 1 or page_num > len(pdf_reader.pages):
                    return Response({'error': f'Page {page_num} hors limites'}, status=status.HTTP_400_BAD_REQUEST)
                pdf_writer.add_page(pdf_reader.pages[page_num - 1])

            output = BytesIO()
            pdf_writer.write(output)
            output.seek(0)

            new_pdf = PDF.objects.create(
                titre=f"Extrait de {pdf.titre}",
                total_pages=len(pages_to_extract),
                categorie=pdf.categorie,
                etat=pdf.etat,
                patient_associé=pdf.patient_associé
            )
            new_file_name = f"extrait_{pdf.file.name.replace('.pdf', '')}_extracted.pdf"
            new_pdf.file.save(new_file_name, output)

            return Response({'message': 'Pages extraites avec succès', 'new_pdf_id': new_pdf.id}, status=status.HTTP_201_CREATED)
        except PDF.DoesNotExist:
            return Response({'error': 'PDF non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)