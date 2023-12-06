# Generated by Django 4.1.11 on 2023-10-02 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0027_project_company'),
        ('actions', '0025_action_alpha_action_beta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=256)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actions.action')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]