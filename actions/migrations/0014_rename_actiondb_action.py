# Generated by Django 4.2.3 on 2023-08-11 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0023_messageblock_html'),
        ('agents', '0005_agentdb_description'),
        ('actions', '0013_rename_actionformelement_actionelement'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ActionDB',
            new_name='Action',
        ),
    ]