# Generated by Django 4.1.11 on 2023-09-26 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruction', '0026_instructiontype_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructionelementagentcall',
            name='stream',
            field=models.BooleanField(default=False),
        ),
    ]