# Generated by Django 4.1.3 on 2023-04-03 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0067_storylinecharacter_bio_raw_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='storylinecharacter',
            name='team_raw',
            field=models.TextField(null=True),
        ),
    ]