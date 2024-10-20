from rest_framework import serializers
from .models import PDF

class AffichpdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF
        fields = ['id', 'titre', 'total_pages', 'categorie', 'etat', 'file']
