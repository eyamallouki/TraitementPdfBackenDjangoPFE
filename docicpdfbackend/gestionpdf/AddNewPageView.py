from io import BytesIO
from PIL import Image  # Pillow pour la gestion des images
from PyPDF2.errors import PdfReadError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import PDF
from PyPDF2 import PdfWriter, PdfReader
import logging

# Création d'un logger pour suivre les erreurs
logger = logging.getLogger(__name__)

class AddNewPageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pdf_id):
        new_page_file = request.FILES.get('new_page')  # Récupération du fichier uploadé
        if new_page_file is None:
            return Response({'error': 'Aucun nouveau fichier de page fourni'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Récupération du fichier PDF existant
            pdf = get_object_or_404(PDF, id=pdf_id)
            pdf_reader = PdfReader(pdf.file.path)

            pdf_writer = PdfWriter()

            # Ajout des pages du PDF existant
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            # Détection du type de fichier : PDF ou image
            if new_page_file.name.endswith('.pdf'):
                # Si c'est un fichier PDF, on l'ajoute directement
                try:
                    new_page_reader = PdfReader(new_page_file)
                    for page in new_page_reader.pages:
                        pdf_writer.add_page(page)
                except PdfReadError:
                    logger.error("Erreur lors de la lecture du nouveau fichier PDF.")
                    return Response({'error': 'Le fichier de la nouvelle page est invalide ou corrompu.'}, status=status.HTTP_400_BAD_REQUEST)

            elif new_page_file.name.endswith(('.jpg', '.jpeg', '.png')):
                # Si c'est une image, on la convertit en page PDF
                try:
                    image = Image.open(new_page_file)
                    img_byte_arr = BytesIO()
                    image.convert('RGB').save(img_byte_arr, format='PDF')
                    img_byte_arr.seek(0)
                    image_pdf_reader = PdfReader(img_byte_arr)
                    for page in image_pdf_reader.pages:
                        pdf_writer.add_page(page)
                except Exception as e:
                    logger.error(f"Erreur lors de la conversion de l'image en PDF: {e}")
                    return Response({'error': 'Erreur lors de la conversion de l\'image en PDF.'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'error': 'Le type de fichier n\'est pas supporté. Veuillez uploader un fichier PDF ou une image.'}, status=status.HTTP_400_BAD_REQUEST)

            # Création du nouveau fichier PDF avec la page ou l'image ajoutée
            output = BytesIO()
            pdf_writer.write(output)
            output.seek(0)

            original_file_name = pdf.file.name
            new_file_name = original_file_name.replace('.pdf', '') + '_newpageadded.pdf'
            pdf.file.save(new_file_name, output)

            # Mise à jour des informations du PDF
            pdf.total_pages += 1  # Mise à jour du nombre total de pages
            pdf.date_modification = timezone.now()
            pdf.save()

            return Response({'message': 'Nouvelle page ajoutée avec succès'}, status=status.HTTP_200_OK)

        except PDF.DoesNotExist:
            logger.error(f"PDF avec id {pdf_id} non trouvé.")
            return Response({'error': 'PDF non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Une erreur inattendue s'est produite : {e}")
            return Response({'error': 'Une erreur est survenue lors de l\'ajout de la page.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
