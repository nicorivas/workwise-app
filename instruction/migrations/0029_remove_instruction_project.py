# Generated by Django 4.1.11 on 2023-10-03 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instruction', '0028_instruction_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instruction',
            name='project',
        ),
    ]
