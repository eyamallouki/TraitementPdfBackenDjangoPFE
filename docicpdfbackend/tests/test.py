from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from docicpdfbackend.gestionpdf.models import PDF, ExtractedImage

class OCRProcessViewTests(APITestCase):
    def setUp(self):
        # Create a PDF object for testing with the correct media path
        self.pdf = PDF.objects.create(
            titre='Test PDF',
            file='media/pdfs/test.pdf'  # Ensure this path is valid and the file exists
        )

    def test_ocr_process(self):
        url = reverse('ocr_process_view', args=[self.pdf.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('image' in response.data[0])  # Adjust based on your response structure

class CropImageViewTests(APITestCase):
    def setUp(self):
        # Create an ExtractedImage object for testing with the correct media path
        self.pdf = PDF.objects.create(
            titre='Test PDF',
            file='media/pdfs/test.pdf'  # Ensure this path is valid and the file exists
        )
        self.extracted_image = ExtractedImage.objects.create(
            pdf_document=self.pdf,
            image='media/pdfs/image.png',  # Ensure this path is valid
            page_number=1
        )

    def test_crop_image(self):
        url = reverse('crop_image_view', args=[self.extracted_image.id])
        # Prepare your cropped image data here
        cropped_image_data = 'data:image/png;base64,...'  # Provide a valid base64 string
        response = self.client.post(url, {'cropped_image': cropped_image_data})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('file_url' in response.data)

# Add similar test cases for other views and functionality
