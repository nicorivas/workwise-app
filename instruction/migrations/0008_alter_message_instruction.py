# Generated by Django 4.2.3 on 2023-08-21 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instruction', '0007_message_messageblock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='instruction',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='instruction.instruction'),
            preserve_default=False,
        ),
    ]