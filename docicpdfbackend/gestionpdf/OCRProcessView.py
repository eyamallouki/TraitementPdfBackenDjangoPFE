import base64
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PDF, ExtractedImage
from .ExtractedImageSerializer import ExtractedImageSerializer
from pdf2image import convert_from_path
from django.core.files.base import ContentFile
import io
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class OCRProcessView(APIView):
    def post(self, request, pdf_id):
        try:
            # Fetch the PDF document by id
            pdf_document = PDF.objects.get(id=pdf_id)
            # Convert PDF pages to images
            pages = convert_from_path(pdf_document.file.path)

            extracted_images = []
            base_url = request.build_absolute_uri('/pdf/media/extracted_images/')

            # Iterate over each page and save it as an image
            for i, page in enumerate(pages):
                image_file_name = f'{pdf_document.titre}_page_{i + 1}.png'
                image_path = os.path.join('media/extracted_images', image_file_name)

                # Save the image on disk
                page.save(image_path, 'PNG')

                # Create ExtractedImage entry
                with open(image_path, 'rb') as f:
                    image = ExtractedImage.objects.create(
                        pdf_document=pdf_document,
                        image=ContentFile(f.read(), name=image_file_name),
                        page_number=i + 1
                    )
                    # Append image data to extracted_images
                    extracted_images.append({
                        'id': image.id,
                        'image': f'{base_url}{image_file_name}',
                        'page_number': i + 1
                    })

            return Response(extracted_images, status=status.HTTP_201_CREATED)

        except PDF.DoesNotExist:
            logger.error(f"PDF with id {pdf_id} does not exist.")
            return Response({'error': 'PDF document not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error during OCR process: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CropImageView(APIView):
    def post(self, request, image_id):
        try:
            extracted_image = ExtractedImage.objects.get(id=image_id)

            crop_coordinates = request.data.get('crop_coordinates')
            cropped_image_base64 = request.data.get('cropped_image')

            if not crop_coordinates or not cropped_image_base64:
                return Response({'error': 'Invalid data provided.'}, status=status.HTTP_400_BAD_REQUEST)

            # Decode the base64 cropped image
            format, imgstr = cropped_image_base64.split(';base64,')
            image_data = base64.b64decode(imgstr)

            # Load the cropped image using PIL
            cropped_image = Image.open(io.BytesIO(image_data))

            # Save the cropped image
            cropped_image_io = io.BytesIO()
            cropped_image.save(cropped_image_io, format='PNG')  # Save as PNG
            cropped_image_file = ContentFile(cropped_image_io.getvalue(), name=f'cropped_{extracted_image.image.name}')

            # Update the model with the cropped image
            extracted_image.image.save(f'cropped_{extracted_image.image.name}', cropped_image_file, save=True)
            extracted_image.crop_coordinates = crop_coordinates
            extracted_image.save()

            return Response({
                'message': 'Cropped image saved successfully',
                'fileType': 'png',  # Or 'jpg' based on the type
                'file_url': extracted_image.image.url
            }, status=status.HTTP_200_OK)

        except ExtractedImage.DoesNotExist:
            return Response({'error': 'Image not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

