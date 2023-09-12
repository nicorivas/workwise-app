# Generated by Django 4.2.3 on 2023-09-11 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_company_strategy'),
        ('user', '0005_remove_profile_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='companies',
            field=models.ManyToManyField(blank=True, null=True, to='company.company'),
        ),
    ]
