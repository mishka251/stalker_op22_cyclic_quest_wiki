# Generated by Django 4.1.3 on 2023-03-30 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0059_dialog_init_func_raw'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialog',
            name='comments_raw',
            field=models.TextField(null=True),
        ),
    ]
