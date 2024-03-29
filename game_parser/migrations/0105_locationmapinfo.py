# Generated by Django 4.2 on 2024-01-25 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0104_inventorybox_itemintreasurebox'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationMapInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('texture_raw', models.CharField(max_length=255)),
                ('bound_rect_raw', models.CharField(max_length=255)),
                ('global_rect_raw', models.CharField(max_length=255)),
                ('weathers', models.CharField(max_length=255)),
                ('music_tracks', models.CharField(max_length=255)),
                ('map_image', models.ImageField(null=True, upload_to='')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game_parser.location')),
            ],
        ),
    ]
