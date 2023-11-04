# Generated by Django 4.2.3 on 2023-09-11 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_company_strategy'),
        ('projects', '0026_project_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='company.company'),
            preserve_default=False,
        ),
    ]