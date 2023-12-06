# Generated by Django 4.1.11 on 2023-12-04 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruction', '0040_instructiontype_flow_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructionelement',
            name='flow_description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='instructionelement',
            name='flow_title',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
