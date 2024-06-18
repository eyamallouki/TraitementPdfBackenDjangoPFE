from rest_framework import serializers
from .models import PDF, Page

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['numéro', 'orientation']

class PDFDetailSerializer(serializers.ModelSerializer):
    pdf_pages = PageSerializer(many=True, read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = PDF
        fields = ['titre', 'total_pages', 'categorie', 'etat', 'file_url', 'pdf_pages']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
