# Generated by Django 4.1.3 on 2023-04-03 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game_parser", "0068_storylinecharacter_team_raw"),
    ]

    operations = [
        migrations.AlterField(
            model_name="icon",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
    ]
