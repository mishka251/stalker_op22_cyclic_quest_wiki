# Generated by Django 4.2 on 2024-02-03 07:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game_parser", "0109_spawnitem_location"),
    ]

    operations = [
        migrations.CreateModel(
            name="Monster",
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
                ("section_name", models.CharField(max_length=255)),
                ("short_name", models.CharField(max_length=255)),
                ("visual_str", models.CharField(max_length=255)),
                ("corpse_visual_str", models.CharField(max_length=255)),
                ("icon_str", models.CharField(max_length=255)),
                (
                    "Spawn_Inventory_Item_Section",
                    models.CharField(max_length=255, null=True),
                ),
                (
                    "Spawn_Inventory_Item_Probability",
                    models.CharField(max_length=255, null=True),
                ),
                ("class_name", models.CharField(max_length=255, null=True)),
                ("terrain", models.CharField(max_length=255, null=True)),
                ("species", models.CharField(max_length=255, null=True)),
                ("spec_rank", models.CharField(max_length=255, null=True)),
            ],
            options={
                "verbose_name": "Мутант",
                "verbose_name_plural": "Мутанты",
            },
        ),
        migrations.AlterField(
            model_name="gamestoryid",
            name="character",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="game_parser.storylinecharacter",
            ),
        ),
        migrations.AlterField(
            model_name="gamestoryid",
            name="item",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="game_parser.baseitem",
            ),
        ),
        migrations.AlterField(
            model_name="gamestoryid",
            name="spawn_section",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="game_parser.spawnitem",
            ),
        ),
        migrations.AlterField(
            model_name="gamestoryid",
            name="spawn_section_custom",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="game_parser.customspawnitem",
            ),
        ),
        migrations.AlterField(
            model_name="gamestoryid",
            name="treasure",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="game_parser.treasure",
            ),
        ),
        migrations.AlterField(
            model_name="spawnitem",
            name="character_profile",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="game_parser.storylinecharacter",
                verbose_name="Профиль НПС",
            ),
        ),
        migrations.AlterField(
            model_name="spawnitem",
            name="character_profile_str",
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                verbose_name="Профиль сталкера",
            ),
        ),
        migrations.AlterField(
            model_name="spawnitem",
            name="item",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="game_parser.baseitem",
                verbose_name="Предмет",
            ),
        ),
        migrations.AlterField(
            model_name="spawnitem",
            name="location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="game_parser.location",
            ),
        ),
        migrations.AlterField(
            model_name="spawnitem",
            name="npc_logic",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="game_parser.npclogicconfig",
                verbose_name="Конфиг логики НПС",
            ),
        ),
    ]
