# Generated by Django 4.2.3 on 2023-07-22 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='actiondb',
            name='instruction',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
