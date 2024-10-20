# Generated by Django 5.0.4 on 2024-07-07 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionpdf', '0012_remove_pdf_image_remove_pdf_signature_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='pdfs/')),
            ],
        ),
        migrations.AddField(
            model_name='pdf',
            name='images',
            field=models.ManyToManyField(to='gestionpdf.image'),
        ),
    ]
