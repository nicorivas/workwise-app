# Generated by Django 4.1.11 on 2023-11-08 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pitch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=256)),
                ('author_email', models.EmailField(max_length=254)),
                ('startup_name', models.CharField(max_length=256)),
                ('startup_level', models.CharField(choices=[('1', 'Idea'), ('2', 'Prototipo'), ('3', 'Constituido'), ('4', 'Escalamiento')], default='1', max_length=1)),
                ('pitch', models.TextField()),
                ('pitch_prompt', models.TextField()),
                ('pitch_analysis_short', models.TextField()),
                ('pitch_analysis_long', models.TextField()),
            ],
        ),
    ]
