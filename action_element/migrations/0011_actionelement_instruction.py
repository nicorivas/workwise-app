# Generated by Django 4.2.3 on 2023-08-21 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instruction', '0003_remove_instruction_prompt'),
        ('action_element', '0010_rename_mimesis_class_actionelementagentcall_mimesis_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionelement',
            name='instruction',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='instruction.instruction'),
            preserve_default=False,
        ),
    ]