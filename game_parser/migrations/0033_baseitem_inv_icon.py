# Generated by Django 4.1.3 on 2022-12-26 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game_parser", "0032_baseitem_description_translation_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="baseitem",
            name="inv_icon",
            field=models.ImageField(
                null=True,
                upload_to="item_icons/",
                verbose_name="Иконка в инвентаре",
            ),
        ),
    ]
