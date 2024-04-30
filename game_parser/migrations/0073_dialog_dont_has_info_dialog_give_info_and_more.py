# Generated by Django 4.2 on 2023-04-05 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game_parser", "0072_basescriptreward_polymorphic_ctype"),
    ]

    operations = [
        migrations.AddField(
            model_name="dialog",
            name="dont_has_info",
            field=models.ManyToManyField(related_name="close_dialogs", to="game_parser.infoportion", verbose_name="Информация, блокирующая диалог"),
        ),
        migrations.AddField(
            model_name="dialog",
            name="give_info",
            field=models.ManyToManyField(related_name="activated_in_dialogs", to="game_parser.infoportion", verbose_name="Информация, получаемая за диалог"),
        ),
        migrations.AddField(
            model_name="dialog",
            name="has_info",
            field=models.ManyToManyField(related_name="open_dialogs", to="game_parser.infoportion", verbose_name="Информация, нужная для получения диалога"),
        ),
        migrations.AddField(
            model_name="dialog",
            name="init_func",
            field=models.ManyToManyField(related_name="dialogs_inited", to="game_parser.scriptfunction", verbose_name="функция, инициализирующая диалог"),
        ),
        migrations.AddField(
            model_name="dialog",
            name="precondition",
            field=models.ManyToManyField(related_name="dialogs_required_function", to="game_parser.scriptfunction", verbose_name="Функции-условия для диалога"),
        ),
        migrations.AddField(
            model_name="dialogphrase",
            name="actions",
            field=models.ManyToManyField(related_name="starts_phrases", to="game_parser.scriptfunction", verbose_name="Функции,запускаемые диалогом"),
        ),
        migrations.AddField(
            model_name="dialogphrase",
            name="disable",
            field=models.ManyToManyField(related_name="disable_phrases", to="game_parser.infoportion", verbose_name="Убираемые инфопоршни?"),
        ),
        migrations.AddField(
            model_name="dialogphrase",
            name="disable_info",
            field=models.ManyToManyField(related_name="disable_info_in_phrases", to="game_parser.infoportion", verbose_name="Убираемые инфопоршни?"),
        ),
        migrations.AddField(
            model_name="dialogphrase",
            name="don_has_info",
            field=models.ManyToManyField(related_name="close_phrases", to="game_parser.infoportion", verbose_name="Информация, блокирующая фразу диалог"),
        ),
        migrations.AddField(
            model_name="dialogphrase",
            name="give_info",
            field=models.ManyToManyField(related_name="activated_in_phrases", to="game_parser.infoportion", verbose_name="Информация, получаемая за фразу диалог"),
        ),
        migrations.AddField(
            model_name="dialogphrase",
            name="has_info",
            field=models.ManyToManyField(related_name="open_phrases", to="game_parser.infoportion", verbose_name="Информация, нужная для получения фразы диалога"),
        ),
        migrations.AddField(
            model_name="dialogphrase",
            name="precondition",
            field=models.ManyToManyField(related_name="phrase_required_function", to="game_parser.scriptfunction", verbose_name="Функции-условия для фразы диалога"),
        ),
        migrations.AddField(
            model_name="infoportion",
            name="actions",
            field=models.ManyToManyField(related_name="starts_infoportions", to="game_parser.scriptfunction", verbose_name="Функции,запускаемые инфопоршнем"),
        ),
    ]
