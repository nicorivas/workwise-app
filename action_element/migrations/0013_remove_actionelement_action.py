# Generated by Django 4.2.3 on 2023-08-21 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('action_element', '0012_remove_actionelement_instruction_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actionelement',
            name='action',
        ),
    ]
