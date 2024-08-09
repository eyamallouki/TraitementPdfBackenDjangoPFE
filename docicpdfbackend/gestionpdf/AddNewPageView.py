from io import BytesIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import PDF
from PyPDF2 import PdfWriter, PdfReader

class AddNewPageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pdf_id):
        new_page_file = request.FILES.get('new_page')
        if new_page_file is None:
            return Response({'error': 'Aucun nouveau fichier de page fourni'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pdf = get_object_or_404(PDF, id=pdf_id)
            pdf_reader = PdfReader(pdf.file.path)
            new_page_reader = PdfReader(new_page_file)
            pdf_writer = PdfWriter()

            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            for page in new_page_reader.pages:
                pdf_writer.add_page(page)

            output = BytesIO()
            pdf_writer.write(output)
            output.seek(0)

            original_file_name = pdf.file.name
            new_file_name = original_file_name.replace('.pdf', '') + '_newpageadded.pdf'
            pdf.file.save(new_file_name, output)
            pdf.total_pages += len(new_page_reader.pages)
            pdf.date_modification = timezone.now()
            pdf.save()

            return Response({'message': 'Nouvelle page ajoutée avec succès'}, status=status.HTTP_200_OK)
        except PDF.DoesNotExist:
            return Response({'error': 'PDF non trouvé'}, status=status.HTTP_404_NOT_FOUND)