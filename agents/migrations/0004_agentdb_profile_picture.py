# Generated by Django 4.2.3 on 2023-08-02 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0003_agentdb_short_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentdb',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='agents'),
        ),
    ]
