# Generated by Django 4.2 on 2024-01-12 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0088_rename_character_profile_spawnitem_character_profile_str'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spawnitem',
            name='custom_data',
            field=models.TextField(null=True),
        ),
    ]
