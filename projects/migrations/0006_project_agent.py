# Generated by Django 4.2.3 on 2023-07-22 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0002_traitdb_personalitydb_agentdb_personality'),
        ('projects', '0005_message_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agents.agentdb'),
        ),
    ]
