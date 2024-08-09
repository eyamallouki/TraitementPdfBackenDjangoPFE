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
        # Attendez une liste de numéros de pages dans l'ordre souhaité
        new_order = request.data.get('new_order')

        if not new_order:
            return Response({'error': 'new_order est requis'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pdf = get_object_or_404(PDF, id=pdf_id)
            pdf_reader = PdfReader(pdf.file.path)
            pdf_writer = PdfWriter()

            # Vérifiez que tous les indices sont valides
            if any(page < 1 or page > len(pdf_reader.pages) for page in new_order):
                return Response({'error': 'Numéro de page invalide dans new_order'}, status=status.HTTP_400_BAD_REQUEST)

            # Réorganise les pages selon new_order
            new_pages = [pdf_reader.pages[i - 1] for i in new_order]

            for page in new_pages:
                pdf_writer.add_page(page)

            output = BytesIO()
            pdf_writer.write(output)
            output.seek(0)

            original_file_name = pdf.file.name
            new_file_name = original_file_name.replace('.pdf', '') + '_reordered.pdf'
            pdf.file.save(new_file_name, output)
            pdf.date_modification = timezone.now()
            pdf.save()

            return Response({'message': 'Pages réorganisées avec succès'}, status=status.HTTP_200_OK)
        except PDF.DoesNotExist:
            return Response({'error': 'PDF non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        except IndexError:
            return Response({'error': 'Index de page hors limites'}, status=status.HTTP_400_BAD_REQUEST)
