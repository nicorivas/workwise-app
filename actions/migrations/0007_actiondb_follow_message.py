# Generated by Django 4.2.3 on 2023-07-30 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0006_actionformelement_guide'),
    ]

    operations = [
        migrations.AddField(
            model_name='actiondb',
            name='follow_message',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
