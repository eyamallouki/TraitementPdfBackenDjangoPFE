from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import PDF
from .uploadfileSezeializer import PDFUploadSerializer

class PDFUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.data['patient_associé'] = request.user.id
        file_serializer = PDFUploadSerializer( data=request.data )
        if file_serializer.is_valid():
            file_serializer.save()
            return Response( file_serializer.data, status=status.HTTP_201_CREATED )
        else:
            return Response( file_serializer.errors, status=status.HTTP_400_BAD_REQUEST )