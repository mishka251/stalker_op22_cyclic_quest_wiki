# Generated by Django 4.1.3 on 2023-03-29 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0058_dialog_precondition_raw_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialog',
            name='init_func_raw',
            field=models.TextField(null=True),
        ),
    ]
