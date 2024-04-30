# Generated by Django 4.1.3 on 2022-12-06 21:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game_parser", "0009_alter_baseitem_inv_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Addon",
            fields=[
                ("baseitem_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="game_parser.baseitem")),
            ],
            bases=("game_parser.baseitem",),
        ),
        migrations.CreateModel(
            name="Explosive",
            fields=[
                ("baseitem_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="game_parser.baseitem")),
            ],
            bases=("game_parser.baseitem",),
        ),
        migrations.CreateModel(
            name="Grenade",
            fields=[
                ("baseitem_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="game_parser.baseitem")),
            ],
            bases=("game_parser.baseitem",),
        ),
        migrations.CreateModel(
            name="Knife",
            fields=[
                ("baseitem_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="game_parser.baseitem")),
            ],
            bases=("game_parser.baseitem",),
        ),
    ]
