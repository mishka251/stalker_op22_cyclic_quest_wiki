# Generated by Django 4.2 on 2024-04-03 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("game_parser", "0137_stalkersection_singlestalkerspawnitem_respawn"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cyclicquest",
            name="target_stalker",
        ),
    ]
