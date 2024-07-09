from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .models import PDF
from .uploadfileSezeializer import PDFUploadSerializer, ImageSerializer


class PDFUploadView( APIView ):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = PDFUploadSerializer( data=request.data )
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status=status.HTTP_201_CREATED )
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pdf_images(request, pdf_id):
    pdf = get_object_or_404(PDF, pk=pdf_id)
    images = pdf.images.all()
    serializer = ImageSerializer(images, many=True, context={'request': request})
    return Response({'images': serializer.data})
