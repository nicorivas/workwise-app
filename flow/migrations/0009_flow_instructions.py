# Generated by Django 4.1.11 on 2023-11-28 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruction', '0038_remove_instructionelementrevision_document_element_and_more'),
        ('flow', '0008_flow_debug'),
    ]

    operations = [
        migrations.AddField(
            model_name='flow',
            name='instructions',
            field=models.ManyToManyField(blank=True, to='instruction.instruction'),
        ),
    ]