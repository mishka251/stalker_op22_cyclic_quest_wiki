# Generated by Django 4.2 on 2024-03-03 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0130_alter_anomaly_section_name_alter_character_game_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storylinecharacter',
            name='game_id',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
