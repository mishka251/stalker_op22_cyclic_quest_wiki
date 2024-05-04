# Generated by Django 4.1.3 on 2022-12-12 20:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game_parser", "0021_outfit"),
    ]

    operations = [
        migrations.CreateModel(
            name="Artefact",
            fields=[
                (
                    "baseitem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="game_parser.baseitem",
                    ),
                ),
                (
                    "inventory_radiation",
                    models.DecimalField(
                        decimal_places=6,
                        max_digits=10,
                        null=True,
                        verbose_name="Радиоактивность",
                    ),
                ),
                (
                    "health_restore_speed",
                    models.DecimalField(
                        decimal_places=6,
                        max_digits=10,
                        null=True,
                        verbose_name="Восстановление здоровья?",
                    ),
                ),
                (
                    "burn_immunity",
                    models.DecimalField(
                        decimal_places=3,
                        max_digits=5,
                        verbose_name="Защита от ???",
                    ),
                ),
                (
                    "strike_immunity",
                    models.DecimalField(
                        decimal_places=3,
                        max_digits=5,
                        verbose_name="Защита от ???",
                    ),
                ),
                (
                    "shock_immunity",
                    models.DecimalField(
                        decimal_places=3,
                        max_digits=5,
                        verbose_name="Защита от ???",
                    ),
                ),
                (
                    "wound_immunity",
                    models.DecimalField(
                        decimal_places=3,
                        max_digits=5,
                        verbose_name="Защита от ???",
                    ),
                ),
                (
                    "radiation_immunity",
                    models.DecimalField(
                        decimal_places=3,
                        max_digits=5,
                        verbose_name="Защита от радиации",
                    ),
                ),
                (
                    "telepatic_immunity",
                    models.DecimalField(
                        decimal_places=3,
                        max_digits=5,
                        verbose_name="Защита от телепатии",
                    ),
                ),
                (
                    "chemical_burn_immunity",
                    models.DecimalField(
                        decimal_places=3,
                        max_digits=5,
                        verbose_name="Защита от химии",
                    ),
                ),
                (
                    "explosion_immunity",
                    models.DecimalField(
                        decimal_places=3,
                        max_digits=5,
                        verbose_name="Защита от взрыва",
                    ),
                ),
                (
                    "fire_wound_immunity",
                    models.DecimalField(
                        decimal_places=3,
                        max_digits=5,
                        verbose_name="Защита от ???",
                    ),
                ),
            ],
            options={
                "verbose_name": "Артефакт",
                "verbose_name_plural": "Артефакты",
            },
            bases=("game_parser.baseitem",),
        ),
    ]
