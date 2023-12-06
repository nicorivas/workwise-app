# Generated by Django 4.1.11 on 2023-12-04 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruction', '0039_alter_instructiontype_style'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructiontype',
            name='flow_description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='instructiontype',
            name='flow_title',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
