# serializers.py
from rest_framework import serializers
from .models import PDF

class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF
        fields = ['id', 'titre', 'categorie', 'etat', 'file', 'date_creation', 'date_modification']
