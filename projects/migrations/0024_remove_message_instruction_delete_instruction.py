# Generated by Django 4.2.3 on 2023-08-19 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0023_messageblock_html'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='instruction',
        ),
        migrations.DeleteModel(
            name='Instruction',
        ),
    ]