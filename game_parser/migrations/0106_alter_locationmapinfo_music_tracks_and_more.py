# Generated by Django 4.2 on 2024-01-25 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0105_locationmapinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationmapinfo',
            name='music_tracks',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='locationmapinfo',
            name='weathers',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
