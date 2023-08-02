# Generated by Django 4.2.3 on 2023-08-02 02:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0004_agentdb_profile_picture'),
        ('actions', '0011_actiondb_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actiondb',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='agents.agentdb'),
        ),
    ]
