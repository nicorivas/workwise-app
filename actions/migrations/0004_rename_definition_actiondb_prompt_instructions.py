# Generated by Django 4.2.3 on 2023-07-22 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0003_rename_instruction_actiondb_definition'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actiondb',
            old_name='definition',
            new_name='prompt_instructions',
        ),
    ]
