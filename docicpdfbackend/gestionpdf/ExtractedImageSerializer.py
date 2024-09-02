from rest_framework import serializers
from .models import ExtractedImage

class ExtractedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedImage
        fields = '__all__'
