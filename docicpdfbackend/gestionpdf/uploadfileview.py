from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .models import PDF
from .uploadfileSezeializer import PDFUploadSerializer


class PDFUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = PDFUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PDFImagesView(APIView):
    def get(self, request, pdf_id):
        pdf = get_object_or_404(PDF, id=pdf_id)
        images = pdf.get_images()
        if images:
            return Response({'images': images})
        return Response({'error': 'No images found for this PDF'}, status=status.HTTP_404_NOT_FOUND)