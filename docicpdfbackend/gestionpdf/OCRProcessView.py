from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PDF, ExtractedImage
from .ExtractedImageSerializer import ExtractedImageSerializer
from pdf2image import convert_from_path
from django.core.files.base import ContentFile
import io
from PIL import Image

class OCRProcessView(APIView):
    def post(self, request, pdf_id):
        try:
            pdf_document = PDF.objects.get(id=pdf_id)
            pages = convert_from_path(pdf_document.file.path)

            extracted_images = []
            for i, page in enumerate(pages):
                image_io = io.BytesIO()
                page.save(image_io, format='PNG')
                image_name = f'{pdf_document.titre}_page_{i+1}.png'
                image_file = ContentFile(image_io.getvalue(), name=image_name)

                extracted_image = ExtractedImage.objects.create(
                    pdf_document=pdf_document,
                    image=image_file,
                    page_number=i + 1,
                    crop_coordinates={}
                )
                extracted_images.append(extracted_image)

            serializer = ExtractedImageSerializer(extracted_images, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PDF.DoesNotExist:
            return Response({'error': 'PDF document not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CropImageView(APIView):
    def post(self, request, image_id):
        try:
            extracted_image = ExtractedImage.objects.get(id=image_id)
            crop_coordinates = request.data.get('crop_coordinates')

            image = Image.open(extracted_image.image.path)
            cropped_image = image.crop((
                crop_coordinates['x'],
                crop_coordinates['y'],
                crop_coordinates['x'] + crop_coordinates['width'],
                crop_coordinates['y'] + crop_coordinates['height']
            ))

            cropped_image_io = io.BytesIO()
            cropped_image.save(cropped_image_io, format='PNG')
            cropped_image_file = ContentFile(cropped_image_io.getvalue(), name=f'cropped_{extracted_image.image.name}')

            extracted_image.image.save(f'cropped_{extracted_image.image.name}', cropped_image_file, save=True)
            extracted_image.crop_coordinates = crop_coordinates
            extracted_image.save()

            serializer = ExtractedImageSerializer(extracted_image)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ExtractedImage.DoesNotExist:
            return Response({'error': 'Image not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
