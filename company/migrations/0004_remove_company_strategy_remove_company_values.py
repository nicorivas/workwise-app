# Generated by Django 4.1.11 on 2023-10-03 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_company_strategy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='strategy',
        ),
        migrations.RemoveField(
            model_name='company',
            name='values',
        ),
    ]