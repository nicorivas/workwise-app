# Generated by Django 4.1.11 on 2023-12-04 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruction', '0042_instructionelement_flow_visible'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructionelement',
            name='flow_visible',
        ),
        migrations.AddField(
            model_name='instructiontype',
            name='flow_visible',
            field=models.BooleanField(default=False),
        ),
    ]