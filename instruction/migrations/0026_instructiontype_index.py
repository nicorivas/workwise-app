# Generated by Django 4.1.11 on 2023-09-26 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruction', '0025_instructionelementdocumentlink_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructiontype',
            name='index',
            field=models.IntegerField(default=0),
        ),
    ]
