from pathlib import Path

from django.core.files import File

from stalker_op22_cyclic_quest_wiki.models import Icon
from stalker_op22_cyclic_quest_wiki_proj import settings

FAKE_ICON_NAME = "icon_qlk0QbB.ico"
FAKE_ICON_URL = f"/media/{FAKE_ICON_NAME}"
FAKE_ICON_WIDTH = 256
FAKE_ICON_HEIGHT = 256


def create_fake_icon() -> Icon:

    try:
        return Icon.objects.get(name="fake")
    except Icon.DoesNotExist:
        icon = Icon(name="fake")
        clear_fake_icon()
        with Path("stalker_op22_cyclic_quest_wiki/static/icons/op_2_2.ico").open(
            mode="rb",
        ) as file:
            icon.icon.save(FAKE_ICON_NAME, File(file), save=True)
        return icon


def clear_fake_icon() -> None:
    fake_icon_path = Path(settings.MEDIA_ROOT) / FAKE_ICON_NAME
    if fake_icon_path.exists():
        fake_icon_path.unlink()


def get_fake_icon_data() -> dict:
    return {
        "url": FAKE_ICON_URL,
        "width": FAKE_ICON_WIDTH,
        "height": FAKE_ICON_HEIGHT,
    }
