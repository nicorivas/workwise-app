# Generated by Django 4.1.11 on 2023-09-21 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0009_remove_document_json_remove_document_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentelement',
            name='index',
            field=models.IntegerField(default=0),
        ),
    ]
