# Generated by Django 4.2.3 on 2023-07-30 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_instruction_previous_instruction'),
    ]

    operations = [
        migrations.AddField(
            model_name='instruction',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]