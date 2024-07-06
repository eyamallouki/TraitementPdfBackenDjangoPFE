# views.py
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import PDF

class ServePDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, filename, *args, **kwargs):
        pdf = get_object_or_404(PDF, file=f'pdfs/{filename}', patient_associé=request.user)
        return FileResponse(pdf.file, content_type='application/pdf')
