from django.db import models
from django.utils import timezone
from gestionuser.models import User

class PDF(models.Model):
    titre = models.CharField(max_length=255)
    total_pages = models.IntegerField(default=0)
    categorie = models.CharField(max_length=255)
    ETAT_CHOICES = [
        ('traité', 'Traité'),
        ('non_traité', 'Non traité'),
    ]
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='non_traité')
    file = models.FileField(upload_to='pdfs/', max_length=255, null=True, blank=True)
    patient_associé = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pdfs')
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)  # Use auto_now for automatic update on modification
    images = models.ManyToManyField('Image', related_name='pdfs')  # Ensure proper related_name usage
    filtered_text = models.TextField(blank=True, null=True)  # Field to store OCR filtered text

    def __str__(self):
        return self.titre

class Image(models.Model):
    file = models.ImageField(upload_to='images/png/')
    page_number = models.IntegerField(default=1)
    pdf = models.ForeignKey(PDF, on_delete=models.CASCADE, related_name='image_files', null=True, blank=True)

    def __str__(self):
        return f"Image from PDF {self.pdf.titre} - Page {self.page_number}"

class Page(models.Model):
    pdf = models.ForeignKey(PDF, on_delete=models.CASCADE, related_name='pdf_pages')
    numéro = models.IntegerField()
    orientation = models.CharField(max_length=50)

    def __str__(self):
        return f"Page {self.numéro} de {self.pdf}"


class ExtractedImage(models.Model):
    pdf_document = models.ForeignKey(PDF, on_delete=models.CASCADE, related_name='extracted_images')
    image = models.ImageField(upload_to='extracted_images/')
    page_number = models.IntegerField()
    crop_coordinates = models.JSONField()  # Store the crop coordinates as JSON
    date_extraction = models.DateTimeField(auto_now_add=True)
    crop_coordinates = models.JSONField( null=True, blank=True )