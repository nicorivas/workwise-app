# Generated by Django 4.2.3 on 2023-07-28 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_documentelement_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentelement',
            name='document',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='document_element',
        ),
        migrations.RemoveField(
            model_name='project',
            name='document',
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.DeleteModel(
            name='DocumentElement',
        ),
    ]