# Generated by Django 4.2.3 on 2023-08-21 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0019_action_mimesis_class'),
        ('instruction', '0003_remove_instruction_prompt'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actions.action')),
                ('previous_instruction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='instruction.instructiontype')),
            ],
        ),
    ]
