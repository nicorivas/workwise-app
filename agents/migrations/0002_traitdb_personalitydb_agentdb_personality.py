# Generated by Django 4.2.3 on 2023-07-20 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TraitDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('category', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=512)),
                ('self_definition', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalityDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('traits', models.ManyToManyField(blank=True, null=True, to='agents.traitdb')),
            ],
        ),
        migrations.AddField(
            model_name='agentdb',
            name='personality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agents.personalitydb'),
        ),
    ]
