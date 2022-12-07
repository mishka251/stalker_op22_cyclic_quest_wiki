from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Optional

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.ltx_parser import LtxParser
from game_parser.models import (Weapon, Ammo, Addon, Knife, Explosive, Grenade, GrenadeLauncher, Scope, Silencer)
from game_parser.models.items.base_item import BaseItem

base_path = settings.OP22_GAME_DATA_PATH


class ModelTypes(Enum):
    WEAPON = 'weapon'
    AMMO = 'ammo'
    ADDON = 'addon'
    UNKNOWN = 'unknown'
    GRENADE = 'grenade'
    KNIFE = 'knife'
    EXPLOSIVE = 'explosive'
    GRENADE_LAUNCHER = 'grenade_launcher'
    FAKE = 'fake'
    SILENCER = 'silencer'
    SCOPE = 'scope'


class Command(BaseCommand):

    def get_root_dir_path(self):
        return base_path / 'config' / 'weapons'

    _excluded_files = {
        base_path / 'config' / 'weapons' / 'ammo.ltx',
        base_path / 'config' / 'weapons' / 'arsenal.ltx',
        base_path / 'config' / 'weapons' / 'explosive.ltx',
        base_path / 'config' / 'weapons' / 'grenade.ltx',
        base_path / 'config' / 'weapons' / 'arsenal_mod' / 'addons',
        base_path / 'config' / 'weapons' / 'knife.ltx',
        base_path / 'config' / 'weapons' / 'upgrade.ltx',
        base_path / 'config' / 'weapons' / 'weapons.ltx',
    }

    _excluded_keys__bolts = {
        'bolt',
        'gilza',
        'bolt_m1',
        'bolt_m2',
    }

    _excluded_keys__stationary_guns = {
        'mounted_weapon',
        'stationary_mgun',
        'stationary_turret',
        'stationary_gauss_turret',
        'turret_mgun',
        'turret_mgun_immunities',
        'turret_army',
        'turret_nato',
        '30_mm_mgun',
    }

    _excluded_keys__soulcube = {
        'soulcube_a',
        'soulcube_0',
        'soulcube_1',
        'soulcube_2',
        'soulcube_3',
        'soulcube_4',
        'soulcube_5',
        'bleeding_heal',
    }

    _excluded_other = {
        'fake_grenades_base',
        'delayed_action_fuse',
        'bomba_babah',
        'bullet_manager',
        'tracers_color_table',
    }

    _excluded_keys = _excluded_keys__bolts | _excluded_keys__stationary_guns | _excluded_keys__soulcube| _excluded_other

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

    def get_files_paths(self):
        return self.get_files_from_dir(self.get_root_dir_path())

    @atomic
    def handle(self, **options):

        Addon.objects.all().delete()
        Ammo.objects.all().delete()
        Explosive.objects.all().delete()
        Grenade.objects.all().delete()
        Knife.objects.all().delete()
        Weapon.objects.all().delete()
        GrenadeLauncher.objects.all().delete()

        known_bases = {
            'WP_AK74': {
                'model_type': ModelTypes.WEAPON,
            },
            'WP_BINOC': {
                'model_type': ModelTypes.WEAPON,
            },
            'WP_BM16': {
                'model_type': ModelTypes.WEAPON,
            },
            'WP_GROZA': {
                'model_type': ModelTypes.WEAPON,
            },
            'WP_HPSA': {
                'model_type': ModelTypes.WEAPON,
            },
            'WP_LR300': {
                'model_type': ModelTypes.WEAPON,
            },
            'WP_PM': {
                'model_type': ModelTypes.WEAPON,
            },
            'WP_RG6': {
                'model_type': ModelTypes.WEAPON,
            },
            'WP_RPG7': {
                'model_type': ModelTypes.WEAPON,
            },
            'WP_SHOTG': {
                'model_type': ModelTypes.WEAPON,
            },
            'WP_SVD': {
                'model_type': ModelTypes.WEAPON,
            },
            'WP_SVU': {
                'model_type': ModelTypes.WEAPON,
            },
            'WP_USP45': {
                'model_type': ModelTypes.WEAPON,
            },
            'WP_VAL': {
                'model_type': ModelTypes.WEAPON,
            },
            'WP_VINT': {
                'model_type': ModelTypes.WEAPON,
            },
            'WP_WALTH': {
                'model_type': ModelTypes.WEAPON,
            },
            'W_MOUNTD': {
                'model_type': ModelTypes.UNKNOWN,
            },
            'W_STMGUN': {
                'model_type': ModelTypes.UNKNOWN,
            },
            'TURRETMG': {
                'model_type': ModelTypes.UNKNOWN,
            },
            'WP_SCOPE': {
                'model_type': ModelTypes.SCOPE,
            },
            'W_SILENC': {
                'model_type': ModelTypes.SILENCER,
            },
            'W_GLAUNC': {
                'model_type': ModelTypes.GRENADE_LAUNCHER,
            },
            'A_OG7B': {
                'model_type': ModelTypes.GRENADE,
            },
            'G_RPG7': {
                'model_type': ModelTypes.GRENADE,
            },
            'knife': {
                'model_type': ModelTypes.KNIFE,
            },
            'knife_hud': {
                'model_type': ModelTypes.UNKNOWN,
            },
            'AMMO': {
                'model_type': ModelTypes.AMMO,
            },
            'G_FAKE': {
                'model_type': ModelTypes.FAKE,
            },
            'G_F1': {
                'model_type': ModelTypes.GRENADE,
            },

            'G_RGD5': {
                'model_type': ModelTypes.GRENADE,
            },

            'A_VOG25': {
                'model_type': ModelTypes.GRENADE,
            },

            'A_M209': {
                'model_type': ModelTypes.GRENADE,
            },

            'II_BOLT': {
                'model_type': ModelTypes.UNKNOWN,
            },

            'O_PHYS_S': {
                'model_type': ModelTypes.UNKNOWN,
            },

            'II_FOOD': {
                'model_type': ModelTypes.UNKNOWN,
            },

            'II_EXPLO': {
                'model_type': ModelTypes.EXPLOSIVE,
            },
            # 'ammo_igl': {},
        }
        files = {
            base_path / 'config' / 'weapons' / 'weapons.ltx',
        }
        # print(*files, sep='\n')
        for index, file in enumerate(files):
            # print(f'process {index+1}/{len(files)} {file}')
            # print()
            parser = LtxParser(file, known_bases)
            results = parser.get_parsed_blocks()

            known_bases |= results

            quest_blocks = {
                k: v
                for k, v in results.items()
                if 'hud' not in k and k not in self._excluded_keys and 'immunities' not in k
            }
            # print(quest_blocks)
            new_models = []
            for quest_name, quest_data in quest_blocks.items():
                # print(f'{quest_name=}')
                model = self._parse_data_to_model(quest_name, quest_data)

                if model is not None:
                    # if quest_data:
                    #     print('unused_data', quest_data)
                    new_models.append(model)

            for ammo in new_models:
                ammo.save()
            print(f'processed {index + 1}/{len(files)} {file}')
            print()
            print()
            print()

    def _parse_data_to_model(self, name: str, data: dict[str, str]) -> Optional[BaseItem]:
        model_type: ModelTypes = data.pop('model_type', None)
        if not model_type:
            print(f'ERROR: no model_type, {name=}')
            return None
        if model_type == ModelTypes.UNKNOWN:
            print(f'WARN: no model_type.UNKNOWN, {name=}')
            return None

        if data.get('fake', False):
            return None

        data.pop('inv_grid_width', None)
        data.pop('inv_grid_height', None)
        data.pop('inv_grid_x', None)
        data.pop('inv_grid_y', None)

        if model_type == ModelTypes.WEAPON:
            return self._weapon_from_dict(name, data)
        if model_type == ModelTypes.AMMO:
            return self._ammo_from_dict(name, data)
        if model_type == ModelTypes.ADDON:
            return self._addon_from_dict(name, data)
        if model_type == ModelTypes.GRENADE:
            return self._grenade_from_dict(name, data)
        if model_type == ModelTypes.KNIFE:
            return self._knife_from_dict(name, data)
        if model_type == ModelTypes.EXPLOSIVE:
            return self._explosive_from_dict(name, data)
        if model_type == ModelTypes.GRENADE_LAUNCHER:
            return self._grenade_launcher_from_dict(name, data)
        if model_type == ModelTypes.SILENCER:
            return self._silencer_from_dict(name, data)
        if model_type == ModelTypes.SCOPE:
            return self._scope_from_dict(name, data)
        if model_type == ModelTypes.FAKE:
            return None
        raise ValueError(f"UNKNOWN {model_type=}")

    def _weapon_from_dict(self, name: str, data: dict[str, str]) -> Weapon:

        ammo = Weapon(
            name=name,
            visual_str=data.pop('visual'),
            description_code=data.pop('description'),
            cost=int(data.pop('cost')),
            inv_name=data.pop('inv_name', None),
            inv_name_short=data.pop('inv_name_short', None),
            inv_weight=Decimal(data.pop('inv_weight')),

            ef_main_weapon_type=data.pop('ef_main_weapon_type', None),
            ef_weapon_type=data.pop('ef_weapon_type', None),
            weapon_class=data.pop('weapon_class', None),
            ammo_mag_size=data.pop('ammo_mag_size'),
            fire_modes_str=data.pop('fire_modes', None),
            ammo_class_str=data.pop('ammo_class'),
            grenade_class_str=data.pop('grenade_class', None),
            rpm=int(data.pop('rpm')),
            scope_status_str=data.pop('scope_status'),
            silencer_status_str=data.pop('silencer_status'),
            grenade_launcher_status=data.pop('grenade_launcher_status'),
            scope_name=data.pop('scope_name', None),
            silencer_name=data.pop('silencer_name', None),
            grenade_launcher_name=data.pop('grenade_launcher_name', None),
        )
        return ammo

    def _ammo_from_dict(self, name: str, data: dict[str, str]) -> Ammo:

        ammo = Ammo(
            name=name,
            visual_str=data.pop('visual'),
            description_code=data.pop('description'),
            cost=int(data.pop('cost')),
            inv_name=data.pop('inv_name'),
            inv_name_short=data.pop('inv_name_short'),
            inv_weight=Decimal(data.pop('inv_weight')),
        )
        return ammo

    def _addon_from_dict(self, name: str, data: dict[str, str]) -> Addon:

        ammo = Addon(
            name=name,
            visual_str=data.pop('visual'),
            description_code=data.pop('description'),
            cost=int(data.pop('cost')),
            inv_name=data.pop('inv_name'),
            inv_name_short=data.pop('inv_name_short', None),
            inv_weight=Decimal(data.pop('inv_weight')),
        )
        return ammo

    def _grenade_from_dict(self, name: str, data: dict[str, str]) -> Grenade:

        ammo = Grenade(
            name=name,
            visual_str=data.pop('visual'),
            description_code=data.pop('description', ""),
            cost=int(data.pop('cost')),
            inv_name=data.pop('inv_name', None),
            inv_name_short=data.pop('inv_name_short', None),
            inv_weight=Decimal(data.pop('inv_weight')),
        )
        return ammo

    def _knife_from_dict(self, name: str, data: dict[str, str]) -> Knife:

        ammo = Knife(
            name=name,
            visual_str=data.pop('visual'),
            description_code=data.pop('description'),
            cost=int(data.pop('cost')),
            inv_name=data.pop('inv_name'),
            inv_name_short=data.pop('inv_name_short'),
            inv_weight=Decimal(data.pop('inv_weight')),
        )
        return ammo

    def _explosive_from_dict(self, name: str, data: dict[str, str]) -> Explosive:

        ammo = Explosive(
            name=name,
            visual_str=data.pop('visual'),
            description_code=data.pop('description', ""),
            cost=int(data.pop('cost')),
            inv_name=data.pop('inv_name'),
            inv_name_short=data.pop('inv_name_short', None),
            inv_weight=Decimal(data.pop('inv_weight')),
        )
        return ammo

    def _grenade_launcher_from_dict(self, name: str, data: dict[str, str]) -> GrenadeLauncher:

        ammo = GrenadeLauncher(
            name=name,
            visual_str=data.pop('visual'),
            description_code=data.pop('description'),
            cost=int(data.pop('cost')),
            inv_name=data.pop('inv_name'),
            inv_name_short=data.pop('inv_name_short', None),
            inv_weight=Decimal(data.pop('inv_weight')),
            ammo_class_str=data.pop('ammo_class', None),
        )
        return ammo

    def _scope_from_dict(self, name: str, data: dict[str, str]) -> Scope:

        ammo = Scope(
            name=name,
            visual_str=data.pop('visual'),
            description_code=data.pop('description', ""),
            cost=int(data.pop('cost')),
            inv_name=data.pop('inv_name'),
            inv_name_short=data.pop('inv_name_short', None),
            inv_weight=Decimal(data.pop('inv_weight')),
        )
        return ammo

    def _silencer_from_dict(self, name: str, data: dict[str, str]) -> Silencer:

        ammo = Silencer(
            name=name,
            visual_str=data.pop('visual'),
            description_code=data.pop('description', ""),
            cost=int(data.pop('cost')),
            inv_name=data.pop('inv_name'),
            inv_name_short=data.pop('inv_name_short', None),
            inv_weight=Decimal(data.pop('inv_weight')),
        )
        return ammo
