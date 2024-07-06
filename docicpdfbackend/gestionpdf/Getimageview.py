from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PDF

class PDFImagesView(APIView):
    def get(self, request, pdf_id):
        try:
            pdf = get_object_or_404(PDF, id=pdf_id)
            images = pdf.get_images()
            if images:
                return Response({'images': images})
            else:
                return Response({'error': 'No images found for this PDF'}, status=status.HTTP_404_NOT_FOUND)
        except PDF.DoesNotExist:
            return Response({'error': 'PDF not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
