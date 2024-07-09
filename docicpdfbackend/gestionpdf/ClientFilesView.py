from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import PDF
from .ClientFilesSerializer import PDFSerializer  #

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient_files(request, patient_id):
    # Récupère tous les fichiers associés au patient spécifié
    pdf_files = []
    txt_files = []
    jpg_files = []
    png_files = []
    other_files = []

    # Filtrer les fichiers par patient
    pdfs = PDF.objects.filter(patient_associé=patient_id)

    for pdf in pdfs:
        if pdf.file:  # Vérifie si le fichier existe et n'est pas None
            file_ext = pdf.file.name.lower()
            if file_ext.endswith('.pdf'):
                pdf_files.append(pdf)
            elif file_ext.endswith('.docx'):
                txt_files.append(pdf)
            elif file_ext.endswith('.jpg'):
                jpg_files.append(pdf)
            elif file_ext.endswith('.png'):
                png_files.append(pdf)
            else:
                other_files.append(pdf)

    response_data = {
        'pdf_files': PDFSerializer(pdf_files, many=True, context={'request': request}).data,
        'txt_files': PDFSerializer(txt_files, many=True, context={'request': request}).data,
        'jpg_files': PDFSerializer(jpg_files, many=True, context={'request': request}).data,
        'png_files': PDFSerializer(png_files, many=True, context={'request': request}).data,
        'other_files': PDFSerializer(other_files, many=True, context={'request': request}).data,
    }
    return Response(response_data, status=status.HTTP_200_OK)
