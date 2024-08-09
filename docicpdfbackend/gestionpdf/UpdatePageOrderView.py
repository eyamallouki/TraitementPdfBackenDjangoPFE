from io import BytesIO
from rest_framework import status
from PyPDF2 import PdfReader, PdfWriter
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import PDF
import fitz  # PyMuPDF
import base64


class GetPdfPagesView( APIView ):
    permission_classes = [IsAuthenticated]

    def get(self, request, pdf_id):
        pdf = get_object_or_404( PDF, id=pdf_id )
        pdf_path = pdf.file.path

        try:
            doc = fitz.open( pdf_path )
            pages = []

            for page_num in range( len( doc ) ):
                page = doc.load_page( page_num )
                pix = page.get_pixmap()
                image_data = pix.tobytes( "png" )

                image_base64 = base64.b64encode( image_data ).decode( 'utf-8' )
                image_url = f"data:image/png;base64,{image_base64}"

                pages.append( {
                    'page_number': page_num + 1,
                    'thumbnail': image_url
                } )

            return Response( pages )
        except Exception as e:
            return Response( {'error': str( e )}, status=500 )


class UpdatePageOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pdf_id):
        new_order = request.data.get('new_order', [])
        if not new_order:
            return Response({'error': 'new_order est requis'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pdf = get_object_or_404(PDF, id=pdf_id)
            pdf_reader = PdfReader(pdf.file.path)
            pdf_writer = PdfWriter()

            if any(page < 1 or page > len(pdf_reader.pages) for page in new_order):
                return Response({'error': 'Numéro de page invalide dans new_order'}, status=status.HTTP_400_BAD_REQUEST)

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

            return Response({'message': 'Pages réorganisées avec succès', 'file_url': pdf.file.url}, status=status.HTTP_200_OK)
        except PDF.DoesNotExist:
            return Response({'error': 'PDF non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        except IndexError:
            return Response({'error': 'Index de page hors limites'}, status=status.HTTP_400_BAD_REQUEST)