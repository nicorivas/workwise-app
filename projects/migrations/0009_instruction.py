# Generated by Django 4.2.3 on 2023-07-22 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0003_rename_instruction_actiondb_definition'),
        ('projects', '0008_project_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.TextField()),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actions.actiondb')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]
