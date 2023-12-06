# Generated by Django 4.1.11 on 2023-09-25 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruction', '0022_message_called'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructionelementtype',
            name='name',
            field=models.CharField(choices=[('MSG', 'Message'), ('TXT', 'Text Input'), ('ACA', 'Agent Call'), ('REV', 'Revision'), ('DOC', 'Document')], default='MSG', max_length=3),
        ),
    ]