# gestionpdf/serializers.py
from rest_framework import serializers
from .models import PDF

class PDFUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF
        fields = ['titre', 'total_pages', 'categorie', 'etat', 'patient_associé', 'file']