# Generated by Django 5.0.4 on 2024-06-13 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionpdf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdf',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='pdfs/'),
        ),
    ]
