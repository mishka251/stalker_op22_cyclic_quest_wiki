# Generated by Django 4.1.3 on 2023-04-02 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0066_storylinecharacter_crouch_type_raw_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='storylinecharacter',
            name='bio_raw',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='storylinecharacter',
            name='terrain_sect_raw',
            field=models.TextField(null=True),
        ),
    ]
