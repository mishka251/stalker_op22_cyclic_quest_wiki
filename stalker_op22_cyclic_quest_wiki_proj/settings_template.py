from .base_settings import *

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ""

OP22_GAME_DATA_PATH = Path(r"")

INSTALLED_APPS += [
    "game_parser",
]