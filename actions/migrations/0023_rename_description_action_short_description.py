# Generated by Django 4.1.11 on 2023-09-13 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0022_remove_action_previous_action'),
    ]

    operations = [
        migrations.RenameField(
            model_name='action',
            old_name='description',
            new_name='short_description',
        ),
    ]
