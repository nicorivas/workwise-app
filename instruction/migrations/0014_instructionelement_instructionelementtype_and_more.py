# Generated by Django 4.2.3 on 2023-09-08 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instruction', '0013_alter_instruction_show_as_possible'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructionElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=256)),
                ('guide', models.TextField(blank=True, null=True)),
                ('instruction_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instruction.instructiontype')),
            ],
        ),
        migrations.CreateModel(
            name='InstructionElementType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('MSG', 'Message'), ('TXT', 'Text Input'), ('ACA', 'Agent Call')], default='MSG', max_length=3)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='InstructionElementAgentCall',
            fields=[
                ('instructionelement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='instruction.instructionelement')),
                ('button_label', models.CharField(default='Submit', max_length=256)),
                ('mimesis_action', models.CharField(blank=True, max_length=256, null=True)),
                ('document_input', models.CharField(blank=True, max_length=256, null=True)),
                ('working_message', models.CharField(blank=True, max_length=256, null=True)),
            ],
            bases=('instruction.instructionelement',),
        ),
        migrations.CreateModel(
            name='InstructionElementMessage',
            fields=[
                ('instructionelement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='instruction.instructionelement')),
                ('message', models.TextField(blank=True, null=True)),
            ],
            bases=('instruction.instructionelement',),
        ),
        migrations.CreateModel(
            name='InstructionElementTextInput',
            fields=[
                ('instructionelement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='instruction.instructionelement')),
                ('message', models.TextField(blank=True, null=True)),
                ('audio', models.BooleanField(default=True)),
            ],
            bases=('instruction.instructionelement',),
        ),
        migrations.AddField(
            model_name='instructionelement',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instruction.instructionelementtype'),
        ),
    ]
