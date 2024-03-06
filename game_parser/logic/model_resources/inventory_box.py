import json
from typing import Any

from django.conf import settings

from game_parser.logic.ltx_parser import LtxParser
from game_parser.logic.model_resources.base_resource import BaseModelResource, SECTION_NAME, CharField
from game_parser.models import InventoryBox, BaseItem, ItemInTreasureBox


class NoSpawnError(ValueError):
    pass


class InventoryBoxResource(BaseModelResource):
    _model_cls = InventoryBox
    _fields = [
        CharField(SECTION_NAME, 'section_name'),
        CharField('custom_data', 'source_file_name'),
        CharField('visual', 'visual_str', required=False),
    ]

    def _apply_data(self, data: dict[str, Any], instance: InventoryBox):
        super()._apply_data(data, instance)
        try:
            treasure_content = self._load_content(instance.source_file_name)
        except NoSpawnError:
            treasure_content = None
        raw_items_str = json.dumps(treasure_content) if treasure_content is not None else None
        instance.items_raw = raw_items_str

    def _save_instance(self, instance):
        super()._save_instance(instance)
        try:
            treasure_content = self._load_content(instance.source_file_name)
        except NoSpawnError:
            return

        for item_name, items_count in treasure_content.items():
            item = BaseItem.objects.filter(name=item_name).first() or BaseItem.objects.filter(
                inv_name=item_name).first()
            if not item:
                print(f"Not found item {item_name=}")
                continue
            ItemInTreasureBox.objects.create(
                item=item,
                box=instance,
                count=items_count,
            )

    def _load_content(self, source_file_name: str) -> dict[str, int]:
        base_path = settings.OP22_GAME_DATA_PATH
        path = base_path / "config" / source_file_name
        try:
            parser = LtxParser(path)
        except FileNotFoundError as e:
            raise NoSpawnError("Нет файла") from e
        results = parser.get_parsed_blocks()

        spawn = results.get("spawn")
        if not spawn:
            raise NoSpawnError("No spawn")
        item_with_count: dict[str, int] = {}
        if isinstance(spawn, list):
            item_with_count = {
                item: 1
                for item in spawn
            }
        elif isinstance(spawn, dict):
            item_with_count = {
                item: item_count if item_count is not None else 1
                for (item, item_count) in spawn.items()
            }
        return item_with_count
