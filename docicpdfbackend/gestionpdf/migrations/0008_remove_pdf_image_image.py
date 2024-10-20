# Generated by Django 5.0.4 on 2024-07-04 10:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionpdf', '0007_remove_pdf_modified_file_modifiedpdf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdf',
            name='image',
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('pdf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='gestionpdf.pdf')),
            ],
        ),
    ]
