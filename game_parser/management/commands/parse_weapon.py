import logging
from enum import Enum
from pathlib import Path
from typing import Optional

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.logic.model_resources.base_item import WeaponResource, BaseItemResource, AmmoResource, GrenadeResource, \
    KnifeResource, ExplosiveResource, GrenadeLauncherResource, SilencerResource, ScopeResource
from game_parser.models import (Weapon, Ammo, Addon, Knife, Explosive, Grenade, GrenadeLauncher)
from game_parser.models.items.base_item import BaseItem

base_path = settings.OP22_GAME_DATA_PATH
logger = logging.getLogger(__name__)


class ModelTypes(Enum):
    WEAPON = "weapon"
    AMMO = "ammo"
    ADDON = "addon"
    UNKNOWN = "unknown"
    GRENADE = "grenade"
    KNIFE = "knife"
    EXPLOSIVE = "explosive"
    GRENADE_LAUNCHER = "grenade_launcher"
    FAKE = "fake"
    SILENCER = "silencer"
    SCOPE = "scope"


class Command(BaseCommand):

    def get_root_dir_path(self) -> Path:
        return base_path / "config" / "weapons"

    _excluded_files = {
        base_path / "config" / "weapons" / "ammo.ltx",
        base_path / "config" / "weapons" / "arsenal.ltx",
        base_path / "config" / "weapons" / "explosive.ltx",
        base_path / "config" / "weapons" / "grenade.ltx",
        base_path / "config" / "weapons" / "arsenal_mod" / "addons",
        base_path / "config" / "weapons" / "knife.ltx",
        base_path / "config" / "weapons" / "upgrade.ltx",
        base_path / "config" / "weapons" / "weapons.ltx",
    }

    _excluded_keys__bolts = {
        "bolt",
        "gilza",
        "bolt_m1",
        "bolt_m2",
    }

    _excluded_keys__stationary_guns = {
        "mounted_weapon",
        "stationary_mgun",
        "stationary_turret",
        "stationary_gauss_turret",
        "turret_mgun",
        "turret_mgun_immunities",
        "turret_army",
        "turret_nato",
        "30_mm_mgun",
    }

    _excluded_keys__soulcube = {
        "soulcube_a",
        "soulcube_0",
        "soulcube_1",
        "soulcube_2",
        "soulcube_3",
        "soulcube_4",
        "soulcube_5",
        "bleeding_heal",
    }

    _excluded_other = {
        "fake_grenades_base",
        "delayed_action_fuse",
        "bomba_babah",
        "bullet_manager",
        "tracers_color_table",
    }

    _excluded_fake = {
        "wpn_fake_missile",
        "wpn_fake_missile1",
        "wpn_fake_missile_fly",
        "wpn_fake_missile2",
        "wpn_fake_drob",
        "wpn_fake_missile28",
        "wpn_fake_missile82",
        "wpn_fake_missile_25he",
        "wpn_fake_missile_25sg",
        "wpn_fake_missile_25fb",
        "wpn_fake_missile_25sn",
        "grenade_f1_fake",
        "grenade_rgd5_fake",
        "grenade_flash_fake",
        "grenade_f1_test",
        "grenade_rgd5_test",
        "grenade_flash_test",
        "gl_test_shell",

        "gl_test_shell_ammo_m209",
        "gl_fake_missile",
        "gl_fake_missile_ammo_m209",
        "gl_test_shell",
        "gl_test_shell_ammo_m209",

        "grenade_gd-05_fake",
        "grenade_gd-05_test",
        "gl_test_shell_ammo_vog-25",
        "gl_test_shell_ammo_vog-25",
        "gl_test_shell_ammo_vog-25p",
        "gl_test_shell_ammo_vog-25p",
        "gl_fake_missile_ammo_vog-25",
        "gl_fake_missile_ammo_vog-25p",
    }

    _excluded_keys = _excluded_keys__bolts | _excluded_keys__stationary_guns | _excluded_keys__soulcube | _excluded_other | _excluded_fake

    def get_files_from_dir(self, path: Path) -> list[Path]:
        files = []
        for child in path.iterdir():
            if child in self._excluded_files:
                continue
            if child.is_file():
                files.append(child)
            else:
                files.extend(self.get_files_from_dir(child))
        return files

    def get_files_paths(self) -> list[Path]:
        return self.get_files_from_dir(self.get_root_dir_path())

    @atomic
    def handle(self, **options) -> None:

        Addon.objects.all().delete()
        Ammo.objects.all().delete()
        Explosive.objects.all().delete()
        Grenade.objects.all().delete()
        Knife.objects.all().delete()
        Weapon.objects.all().delete()
        GrenadeLauncher.objects.all().delete()

        known_bases = {
            "WP_AK74": {
                "model_type": ModelTypes.WEAPON,
            },
            "WP_BINOC": {
                "model_type": ModelTypes.WEAPON,
            },
            "WP_BM16": {
                "model_type": ModelTypes.WEAPON,
            },
            "WP_GROZA": {
                "model_type": ModelTypes.WEAPON,
            },
            "WP_HPSA": {
                "model_type": ModelTypes.WEAPON,
            },
            "WP_LR300": {
                "model_type": ModelTypes.WEAPON,
            },
            "WP_PM": {
                "model_type": ModelTypes.WEAPON,
            },
            "WP_RG6": {
                "model_type": ModelTypes.WEAPON,
            },
            "WP_RPG7": {
                "model_type": ModelTypes.WEAPON,
            },
            "WP_SHOTG": {
                "model_type": ModelTypes.WEAPON,
            },
            "WP_SVD": {
                "model_type": ModelTypes.WEAPON,
            },
            "WP_SVU": {
                "model_type": ModelTypes.WEAPON,
            },
            "WP_USP45": {
                "model_type": ModelTypes.WEAPON,
            },
            "WP_VAL": {
                "model_type": ModelTypes.WEAPON,
            },
            "WP_VINT": {
                "model_type": ModelTypes.WEAPON,
            },
            "WP_WALTH": {
                "model_type": ModelTypes.WEAPON,
            },
            "W_MOUNTD": {
                "model_type": ModelTypes.UNKNOWN,
            },
            "W_STMGUN": {
                "model_type": ModelTypes.UNKNOWN,
            },
            "TURRETMG": {
                "model_type": ModelTypes.UNKNOWN,
            },
            "WP_SCOPE": {
                "model_type": ModelTypes.SCOPE,
            },
            "W_SILENC": {
                "model_type": ModelTypes.SILENCER,
            },
            "W_GLAUNC": {
                "model_type": ModelTypes.GRENADE_LAUNCHER,
            },
            "A_OG7B": {
                "model_type": ModelTypes.GRENADE,
            },
            "G_RPG7": {
                "model_type": ModelTypes.GRENADE,
            },
            "knife": {
                "model_type": ModelTypes.KNIFE,
            },
            "knife_hud": {
                "model_type": ModelTypes.UNKNOWN,
            },
            "AMMO": {
                "model_type": ModelTypes.AMMO,
            },
            "G_FAKE": {
                "model_type": ModelTypes.FAKE,
            },
            "G_F1": {
                "model_type": ModelTypes.GRENADE,
            },

            "G_RGD5": {
                "model_type": ModelTypes.GRENADE,
            },

            "A_VOG25": {
                "model_type": ModelTypes.GRENADE,
            },

            "A_M209": {
                "model_type": ModelTypes.GRENADE,
            },

            "II_BOLT": {
                "model_type": ModelTypes.UNKNOWN,
            },

            "O_PHYS_S": {
                "model_type": ModelTypes.UNKNOWN,
            },

            "II_FOOD": {
                "model_type": ModelTypes.UNKNOWN,
            },

            "II_EXPLO": {
                "model_type": ModelTypes.EXPLOSIVE,
            },
        }
        file = base_path / "config" / "weapons" / "weapons.ltx"

        parser = LtxParser(file, known_bases)
        results = parser.get_parsed_blocks()

        known_bases |= results

        quest_blocks = {
            k: v
            for k, v in results.items()
            if "hud" not in k and k not in self._excluded_keys and "immunities" not in k
        }
        for quest_name, quest_data in quest_blocks.items():
            maybe_instance = self._parse_data_to_model(quest_name, quest_data)
            if maybe_instance is None:
                logger.warning(f"Нет объекта для  {quest_name=}")
                continue
            instance, resource = maybe_instance
            if quest_data:
                logger.warning(f"Для секции {quest_name=} ({resource}) не использованы данные {quest_data}")

    def _parse_data_to_model(self, name: str, data: dict[str, str]) -> Optional[tuple[BaseItem, BaseItemResource]]:
        model_type: ModelTypes = data.pop("model_type", None)
        if not model_type:
            logger.warning(f"ERROR: no model_type, {name=}")
            return None
        if model_type in {ModelTypes.UNKNOWN, ModelTypes.FAKE}:
            logger.warning(f"WARN: no model_type.UNKNOWN, {name=}")
            return None

        if data.get("fake", False):
            return None

        resource = self._get_resource(model_type)
        return resource.create_instance_from_data(name, data), resource

    def _get_resource(self, model_type: ModelTypes) -> BaseItemResource:
        if model_type == ModelTypes.WEAPON:
            return WeaponResource()
        if model_type == ModelTypes.AMMO:
            return AmmoResource()
        if model_type == ModelTypes.GRENADE:
            return GrenadeResource()
        if model_type == ModelTypes.KNIFE:
            return KnifeResource()
        if model_type == ModelTypes.EXPLOSIVE:
            return ExplosiveResource()
        if model_type == ModelTypes.GRENADE_LAUNCHER:
            return GrenadeLauncherResource()
        if model_type == ModelTypes.SILENCER:
            return SilencerResource()
        if model_type == ModelTypes.SCOPE:
            return ScopeResource()
        raise ValueError(f"UNKNOWN {model_type=}")
