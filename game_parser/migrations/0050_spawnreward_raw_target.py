# Generated by Django 4.1.3 on 2023-03-24 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0049_spawnreward_raw_game_vertex_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='spawnreward',
            name='raw_target',
            field=models.CharField(max_length=512, null=True),
        ),
    ]
