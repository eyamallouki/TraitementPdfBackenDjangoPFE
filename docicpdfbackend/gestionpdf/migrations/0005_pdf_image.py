# Generated by Django 5.0.4 on 2024-06-26 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionpdf', '0004_pdf_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdf',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]
