# Generated by Django 4.1.3 on 2023-01-06 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0042_alter_itemintreasure_options_alter_treasure_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='treasure',
            name='name_translation',
        ),
    ]
