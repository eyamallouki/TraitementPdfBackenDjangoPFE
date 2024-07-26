from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from PyPDF2 import PdfReader, PdfWriter
from .models import PDF
from django.utils import timezone

class DeletePagesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pdf_id):
        pdf = get_object_or_404(PDF, id=pdf_id)
        pages_to_delete = request.data.get('pages', [])

        if not isinstance(pages_to_delete, list) or not all(isinstance(page, int) for page in pages_to_delete):
            return Response({'error': 'Liste de pages invalide'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reader = PdfReader(pdf.file.path)
            writer = PdfWriter()

            for page_num in range(len(reader.pages)):
                if page_num + 1 not in pages_to_delete:
                    writer.add_page(reader.pages[page_num])

            output = BytesIO()
            writer.write(output)
            output.seek(0)

            original_file_name = pdf.file.name
            new_file_name = original_file_name.replace('.pdf', '') + '_deletedpages.pdf'
            pdf.file.save(new_file_name, output)
            pdf.date_modification = timezone.now()
            pdf.save()

            return Response({'message': 'Pages supprimées avec succès', 'modified_file': pdf.file.url})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
