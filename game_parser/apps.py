from django.apps import AppConfig


class GameParserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "game_parser"
    verbose_name = "Парсер игровых данных"
