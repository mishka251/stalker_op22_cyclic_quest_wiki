# Generated by Django 4.2 on 2024-01-12 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "game_parser",
            "0086_weapon_ammo_weapon_grenade_launcher_weapon_scope_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="SpawnItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "section_name",
                    models.CharField(max_length=255, verbose_name="Название секции"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                (
                    "position_raw",
                    models.CharField(max_length=300, verbose_name="Координаты(строка)"),
                ),
                (
                    "spawn_id",
                    models.PositiveBigIntegerField(unique=True, verbose_name="ID"),
                ),
                (
                    "game_vertex_id",
                    models.PositiveBigIntegerField(
                        unique=True, verbose_name="vertexID"
                    ),
                ),
                (
                    "location_txt",
                    models.CharField(max_length=255, verbose_name="локация"),
                ),
                ("custom_data", models.TextField()),
                (
                    "character_profile",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Профиль сталкера"
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="game_parser.baseitem",
                        verbose_name="Предмет",
                    ),
                ),
            ],
        ),
    ]
