# Generated by Django 4.2.11 on 2024-04-29 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stalker_op22_cyclic_quest_wiki", "0007_alter_mapposition_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cycletaskvendor",
            name="game_story_id",
            field=models.PositiveIntegerField(
                unique=True,
                verbose_name="ID квестодателя глобальный(story_id)",
            ),
        ),
        migrations.AlterField(
            model_name="cycletaskvendor",
            name="local_id",
            field=models.PositiveIntegerField(
                unique=True,
                verbose_name="ID квестодателя локальный(в cycle_task.ltx)",
            ),
        ),
    ]
