# Generated by Django 4.1.11 on 2023-10-21 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruction', '0037_instructionelementchoices_style'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructionelementrevision',
            name='document_element',
        ),
        migrations.AddField(
            model_name='instructionelementrevision',
            name='document_section_index',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]