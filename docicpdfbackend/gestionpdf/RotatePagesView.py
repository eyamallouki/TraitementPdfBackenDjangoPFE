from io import BytesIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import PDF
from PyPDF2 import PdfWriter, PdfReader
from django.utils import timezone

class RotatePagesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pdf_id):
        pages_to_rotate = request.data.get('pages_to_rotate', [])
        rotation_angle = request.data.get('rotation_angle')

        # Convertir la rotation en entier
        try:
            rotation_angle = int(rotation_angle)
        except ValueError:
            return Response({'error': 'Invalid rotation angle provided'}, status=status.HTTP_400_BAD_REQUEST)

        if not pages_to_rotate or rotation_angle is None:
            return Response({'error': 'pages_to_rotate et rotation_angle sont requis'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pdf = get_object_or_404(PDF, id=pdf_id)
            pdf_reader = PdfReader(pdf.file.path)
            pdf_writer = PdfWriter()

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                if page_num + 1 in pages_to_rotate:
                    page.rotate(rotation_angle)
                pdf_writer.add_page(page)

            output = BytesIO()
            pdf_writer.write(output)
            output.seek(0)

            original_file_name = pdf.file.name
            new_file_name = original_file_name.replace('.pdf', '') + '_rotatedpages.pdf'
            pdf.file.save(new_file_name, output)
            pdf.date_modification = timezone.now()
            pdf.save()

            return Response({'message': 'Pages tournées avec succès', 'modified_file': pdf.file.url}, status=status.HTTP_200_OK)
        except PDF.DoesNotExist:
            return Response({'error': 'PDF non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        except IndexError:
            return Response({'error': 'Index de page hors limites'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
