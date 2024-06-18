from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .PDFDetailSerializer import PDFDetailSerializer
from .models import PDF


class PDFDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        pdf = get_object_or_404(PDF, pk=pk, patient_associé=request.user)
        serializer = PDFDetailSerializer(pdf, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
