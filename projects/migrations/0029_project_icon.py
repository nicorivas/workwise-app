# Generated by Django 4.1.11 on 2023-10-14 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0028_remove_project_action_remove_project_agent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='icon',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
