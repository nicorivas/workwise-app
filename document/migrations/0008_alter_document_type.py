# Generated by Django 4.1.11 on 2023-09-21 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0007_document_imported_document_source_document_source_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='type',
            field=models.CharField(choices=[('PRCH', 'Project Charter'), ('FBGD', 'Feedback Guideline'), ('IMPO', 'Imported Document')], default='PRCH', max_length=4),
        ),
    ]
