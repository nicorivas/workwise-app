# Generated by Django 4.1.11 on 2023-09-26 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0011_documentelement_title'),
        ('instruction', '0023_alter_instructionelementtype_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructionElementDocumentLink',
            fields=[
                ('instructionelement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='instruction.instructionelement')),
                ('document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='document.document')),
            ],
            bases=('instruction.instructionelement',),
        ),
    ]