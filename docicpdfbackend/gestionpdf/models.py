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
    file = models.FileField( upload_to='pdfs/', null=True, blank=True )
    patient_associé = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pdfs')
    date_creation = models.DateTimeField( default=timezone.now )
    date_modification = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return self.titre

class Page(models.Model):
    pdf = models.ForeignKey(PDF, on_delete=models.CASCADE, related_name='pdf_pages')  # Renommez related_name
    numéro = models.IntegerField()
    orientation = models.CharField(max_length=50)

    def __str__(self):
        return f"Page {self.numéro} de {self.pdf}"