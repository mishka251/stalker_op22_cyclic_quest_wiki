# Generated by Django 4.2.11 on 2024-04-13 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stalker_op22_cyclic_quest_wiki", "0004_remove_location_global_rect_raw_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="description_translation",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name="+", to="stalker_op22_cyclic_quest_wiki.translation", verbose_name="Перевод описания"),
        ),
    ]
