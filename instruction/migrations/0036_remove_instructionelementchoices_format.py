# Generated by Django 4.1.11 on 2023-10-12 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instruction', '0035_instructionelementchoices_format'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructionelementchoices',
            name='format',
        ),
    ]