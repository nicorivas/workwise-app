# Generated by Django 4.1.11 on 2023-10-04 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0014_document_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='type',
            field=models.CharField(choices=[('GENE', 'General'), ('PRCH', 'Project Charter'), ('FBGD', 'Feedback Guideline'), ('IMPO', 'Imported Document')], default='PRCH', max_length=4),
        ),
    ]