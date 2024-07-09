
from rest_framework import serializers
from .models import PDF, Image


class PDFUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF
        fields = ['titre', 'total_pages', 'categorie', 'etat', 'patient_associé', 'file']

class ImageSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['file', 'file_url']

    def get_file_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url)