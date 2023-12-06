# Generated by Django 4.1.11 on 2023-09-22 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0011_documentelement_title'),
        ('instruction', '0018_message_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructionelementtype',
            name='name',
            field=models.CharField(choices=[('MSG', 'Message'), ('TXT', 'Text Input'), ('ACA', 'Agent Call'), ('REV', 'Revision')], default='MSG', max_length=3),
        ),
        migrations.CreateModel(
            name='InstructionElementRevision',
            fields=[
                ('instructionelement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='instruction.instructionelement')),
                ('reply', models.TextField(blank=True, null=True)),
                ('document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='document.document')),
                ('document_element', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='document.documentelement')),
            ],
            bases=('instruction.instructionelement',),
        ),
    ]