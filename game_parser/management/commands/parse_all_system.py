import logging
from collections import defaultdict
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from lxml.etree import parse
from PIL import Image

from game_parser.logic.gsc_xml_fixer import GSCXmlFixer
from game_parser.logic.ltx_parser import LtxParser
from game_parser.logic.model_resources.anomaly import AnomalyResource
from game_parser.logic.model_resources.base_item import (
    AmmoResource,
    CapsAnomResource,
    ExplosiveResource,
    GrenadeLauncherResource,
    GrenadeResource,
    KnifeResource,
    MonsterEmbrionResource,
    MonsterPartResource,
    OtherResource,
    OutfitResource,
    ScopeResource,
    SilencerResource,
    TrueArtefactResource,
    WeaponResource,
)
from game_parser.logic.model_resources.base_resource import BaseModelResource
from game_parser.logic.model_resources.inventory_box import InventoryBoxResource
from game_parser.logic.model_resources.monster import MonsterResource
from game_parser.logic.model_xml_loaders.base import BaseModelXmlLoader
from game_parser.logic.model_xml_loaders.dialog import DialogLoader
from game_parser.logic.model_xml_loaders.encyclopedia import EncyclopediaArticleLoader
from game_parser.logic.model_xml_loaders.icon import IconLoader
from game_parser.logic.model_xml_loaders.infoportion import InfoPortionLoader
from game_parser.logic.model_xml_loaders.storyline_character import (
    StorylineCharacterLoader,
)
from game_parser.logic.model_xml_loaders.translation import TranslationLoader
from game_parser.models import (
    Ammo,
    Anomaly,
    CapsAnom,
    Dialog,
    EncyclopediaArticle,
    EncyclopediaGroup,
    Explosive,
    Grenade,
    GrenadeLauncher,
    Icon,
    InfoPortion,
    InventoryBox,
    ItemInTreasureBox,
    Knife,
    Monster,
    MonsterEmbrion,
    MonsterPart,
    Other,
    Outfit,
    Scope,
    Silencer,
    StorylineCharacter,
    Translation,
    TrueArtefact,
    Weapon,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    AMMO_CLASSES = {
        "AMMO",
        "A_M209",
        "A_OG7B",
        "A_VOG25",
    }
    ARTEFACT_classes = {"ARTEFACT"}
    GRENADE_AUNCHED_CLASSES = {
        "W_GLAUNC",
    }

    HANDLE_GRENADES_CLASSES = {
        "G_F1",
        "G_FAKE",
        "G_RGD5",
        "G_RPG7",
    }

    MEDICINE_CLASSES = {
        "II_ANTIR",
        # "II_ATTCH",
        "II_BANDG",
        "II_BOLT",
        "II_BOTTL",
        "II_DOC",
        # "II_EXPLO",
        "II_FOOD",
        "II_MEDKI",
    }

    EXPLOSIVE_CLASSES = {
        "II_EXPLO",
    }

    MONSTERS_CLASSES = {
        "SM_BLOOD",
        "SM_BOARW",
        "SM_BURER",
        "SM_CAT_S",
        "SM_CHIMS",
        "SM_CONTR",
        "SM_DOG_F",
        "SM_DOG_P",
        "SM_DOG_S",
        "SM_FLESH",
        "SM_GIANT",
        "SM_IZLOM",
        "SM_POLTR",
        "SM_P_DOG",
        "SM_SNORK",
        "SM_TUSHK",
        "SM_ZOMBI",
        "AI_PHANT",
    }

    WEAPON_CLASSES = {
        "WP_AK74",
        "WP_BINOC",
        "WP_BM16",
        "WP_GROZA",
        "WP_HPSA",
        "WP_LR300",
        "WP_PM",
        "WP_RG6",
        "WP_RPG7",
        #
        "WP_SHOTG",
        "WP_SVD",
        "WP_SVU",
        "WP_USP45",
        "WP_VAL",
        "WP_VINT",
        "WP_WALTH",
    }

    KNIFE_SECTIONS = {
        "WP_KNIFE",
        "knife",
    }

    SCOPE_CLASSES = {
        "WP_SCOPE",
    }

    ANOMALIES_CLASSES = {
        "ZS_BFUZZ",
        "ZS_BUZZ",
        "ZS_ELECT",
        "ZS_GALAN",
        "ZS_ICE",
        "ZS_MBALD",
        "ZS_MINCE",
        "ZS_RADIO",
        "ZS_ZHARK",
        "Z_AMEBA",
        "Z_MBALD",
        "Z_RUSTYH",
        "Z_NOGRAV",
        "Z_TORRID",
        "Z_ZONE",
    }

    SILENCER_CLASSES = {
        "W_SILENC",
    }

    OUTFITS_CLASSES = {
        "EQU_STLK",
        "EQU_MLTR",
        "EQU_EXO",
        "E_STLK",
        "outfit",
        "without_outfit",
    }

    RESTRICTOR_CLASSES = {
        "SCRIPTZN",
        "SPC_RS_S",
    }

    BREAKEABLE_CLASSES = {
        "O_BRKBL",
        "O_BRKBL_S",
    }

    INV_BOX_CLASSES = {
        "O_INVBOX",
    }

    PNV_CLASSES = {
        "D_NVP",
    }

    OTHER_CLASSES = {
        "II_ATTCH",
        "D_PDA",
        "CL_GBOX",
        "D_SIMDET",
    }

    @atomic
    def handle(self, **options) -> None:
        print("Start cleaning")
        base_path = settings.OP22_GAME_DATA_PATH
        system_file = base_path / "config" / "system.ltx"
        known_bases = {}
        EncyclopediaGroup.objects.all().delete()
        EncyclopediaArticle.objects.all().delete()
        Icon.objects.all().delete()
        StorylineCharacter.objects.all().delete()
        Dialog.objects.all().delete()
        InfoPortion.objects.all().delete()

        while Translation.objects.exists():
            ids = Translation.objects.all()[:1_000].values("id")
            Translation.objects.all().filter(id__in=ids).delete()

        InventoryBox.objects.all().delete()
        ItemInTreasureBox.objects.all().delete()
        Outfit.objects.all().delete()
        Explosive.objects.all().delete()
        Grenade.objects.all().delete()
        Ammo.objects.all().delete()
        Weapon.objects.all().delete()
        Silencer.objects.all().delete()
        Scope.objects.all().delete()
        GrenadeLauncher.objects.all().delete()
        MonsterPart.objects.all().delete()
        Knife.objects.all().delete()
        Other.objects.all().delete()
        TrueArtefact.objects.all().delete()
        MonsterEmbrion.objects.all().delete()
        CapsAnom.objects.all().delete()
        Anomaly.objects.all().delete()
        Monster.objects.all().delete()

        print("Cleaned")

        parser = LtxParser(system_file, known_extends=known_bases)
        results = parser.get_parsed_blocks()
        print("all_system parsed")
        translation_config = results["string_table"]
        translation_files_sources = self._get_paths_list(
            base_path / "config" / "text", translation_config["files"], "xml"
        )

        print(
            "TRANSLATION",
            all(p.exists() for p in translation_files_sources),
            *translation_files_sources,
            sep="\n",
            end="\n" * 3,
        )

        texture_desc_config = results["texture_desc"]
        texture_desc_sources = self._get_paths_list(
            base_path / "config" / "ui", texture_desc_config["files"], "xml"
        )
        print(
            "TEXTURE",
            all(p.exists() for p in texture_desc_sources),
            *texture_desc_sources,
            sep="\n",
            end="\n" * 3,
        )

        info_portions_config = results["info_portions"]
        info_portions_sources = self._get_paths_list(
            base_path / "config" / "gameplay", info_portions_config["files"], "xml"
        )
        print(
            "INFO_PORTION",
            all(p.exists() for p in info_portions_sources),
            *info_portions_sources,
            sep="\n",
            end="\n" * 3,
        )

        encyclopedia_config = results["encyclopedia"]
        encyclopedia_sources = self._get_paths_list(
            base_path / "config" / "gameplay", encyclopedia_config["files"], "xml"
        )
        print(
            "ENCYCLOPEDIA",
            all(p.exists() for p in encyclopedia_sources),
            *encyclopedia_sources,
            sep="\n",
            end="\n" * 3,
        )

        dialogs_config = results["dialogs"]
        dialogs_sources = self._get_paths_list(
            base_path / "config" / "gameplay", dialogs_config["files"], "xml"
        )
        print(
            "DIALOGS",
            all(p.exists() for p in dialogs_sources),
            *dialogs_sources,
            sep="\n",
            end="\n" * 3,
        )

        profiles_config = results["profiles"]
        profiles_sources = self._get_paths_list(
            base_path / "config" / "gameplay", profiles_config["files"], "xml"
        )
        print(
            "PROFILES",
            all(p.exists() for p in profiles_sources),
            *profiles_sources,
            sep="\n",
            end="\n" * 3,
        )

        specific_characters_sources = self._get_paths_list(
            base_path / "config" / "gameplay",
            profiles_config["specific_characters_files"],
            "xml",
        )
        print(
            "SPECIFIC_CHARACTERS",
            all(p.exists() for p in specific_characters_sources),
            *specific_characters_sources,
            sep="\n",
            end="\n" * 3,
        )

        existing_sections_keys = [k for k in results if isinstance(results[k], dict)]

        grouped_by_cls_dict = defaultdict(set)
        for section_name in existing_sections_keys:
            cls_name = results[section_name].get("class", "None")
            grouped_by_cls_dict[cls_name].add(section_name)
        for cls_, keys in grouped_by_cls_dict.items():
            print(cls_, len(keys))

        # TODO Проверить все секции на то, что всё есть в БД
        print("START FILLING")

        self._load_xml(
            translation_files_sources,
            TranslationLoader(),
            "Translation",
            GSCXmlFixer(encoding="utf-8"),
        )
        self._load_icon_xml(texture_desc_sources, "TEXTURE", GSCXmlFixer())
        self._load_xml(
            info_portions_sources, InfoPortionLoader(), "Info", GSCXmlFixer()
        )
        self._load_xml(
            encyclopedia_sources,
            EncyclopediaArticleLoader(),
            "ENCYCLOPEDIA",
            GSCXmlFixer(),
        )
        self._load_xml(dialogs_sources, DialogLoader(), "DIALOGS", GSCXmlFixer())
        self._load_xml(
            specific_characters_sources,
            StorylineCharacterLoader(),
            "SPECIFIC_CHARACTERS",
            GSCXmlFixer(),
        )

        ammo_keys, ammo = self._get_sections_by_class(
            results, grouped_by_cls_dict, self.AMMO_CLASSES
        )
        artefacts_keys, artefacts = self._get_sections_by_class(
            results, grouped_by_cls_dict, self.ARTEFACT_classes
        )
        grenade_launcher_keys, grenade_launcher = self._get_sections_by_class(
            results, grouped_by_cls_dict, self.GRENADE_AUNCHED_CLASSES
        )
        handle_grenade_keys, handle_grenade = self._get_sections_by_class(
            results, grouped_by_cls_dict, self.HANDLE_GRENADES_CLASSES
        )
        medicine_keys, medicine = self._get_sections_by_class(
            results, grouped_by_cls_dict, self.MEDICINE_CLASSES
        )
        monster_keys, monster = self._get_sections_by_class(
            results, grouped_by_cls_dict, self.MONSTERS_CLASSES
        )
        weapon_keys, weapon = self._get_sections_by_class(
            results, grouped_by_cls_dict, self.WEAPON_CLASSES
        )
        anomaly_keys, anomaly = self._get_sections_by_class(
            results, grouped_by_cls_dict, self.ANOMALIES_CLASSES
        )
        scopes_keys, scopes = self._get_sections_by_class(
            results, grouped_by_cls_dict, self.SCOPE_CLASSES
        )
        knife_keys, knife = self._get_sections_by_class(
            results, grouped_by_cls_dict, self.KNIFE_SECTIONS
        )
        silencer_keys, silencer = self._get_sections_by_class(
            results, grouped_by_cls_dict, self.SILENCER_CLASSES
        )
        outfit_keys, outfit = self._get_sections_by_class(
            results, grouped_by_cls_dict, self.OUTFITS_CLASSES
        )
        ibox_keys, iboxes = self._get_sections_by_class(
            results, grouped_by_cls_dict, {"O_INVBOX"}
        )
        monster_parts_keys, monster_parts = self._get_monster_parts(
            results, grouped_by_cls_dict
        )
        explosive_keys, explosive = self._get_explosive(results, grouped_by_cls_dict)

        other_classes = self.MEDICINE_CLASSES | self.PNV_CLASSES | self.OTHER_CLASSES
        other_keys, other = self._get_sections_by_class(
            results, grouped_by_cls_dict, other_classes
        )
        other = {
            key: item
            for key, item in other.items()
            if item.get("monster_part") != "true" and key != "container_basic"
        }

        used_keys = (
            ammo_keys
            | artefacts_keys
            | grenade_launcher_keys
            | handle_grenade_keys
            | medicine_keys
            | monster_keys
            | weapon_keys
            | anomaly_keys
            | scopes_keys
            | knife_keys
            | silencer_keys
            | outfit_keys
            | monster_parts_keys
            | explosive_keys
            | ibox_keys
            | set(other.keys())
        )

        self._load_sections(ammo, AmmoResource())
        self._load_sections(grenade_launcher, GrenadeLauncherResource())
        self._load_sections(handle_grenade, GrenadeResource())
        self._load_sections(weapon, WeaponResource())
        self._load_sections(scopes, ScopeResource())
        self._load_sections(knife, KnifeResource())
        self._load_sections(silencer, SilencerResource())
        self._load_sections(outfit, OutfitResource())
        self._load_sections(monster, MonsterResource())
        self._load_sections(monster_parts, MonsterPartResource())
        self._load_sections(explosive, ExplosiveResource())
        self._load_sections(anomaly, AnomalyResource())
        self._load_sections(other, OtherResource())
        self._load_artefacts(artefacts)
        real_iboxes = {
            ibox_key: ibox_value
            for (ibox_key, ibox_value) in iboxes.items()
            if ibox_value.get("custom_data") is not None
        }
        self._load_sections(real_iboxes, InventoryBoxResource())

        unused_keys = set(existing_sections_keys) - used_keys
        unused_classes = {
            results[section_name].get("class", "None") for section_name in unused_keys
        }
        print(f"UNUSED {len(unused_keys)} {unused_classes=}")

    def _get_explosive(self, results, grouped_by_cls_dict):
        items_keys, items = self._get_sections_by_class(
            results, grouped_by_cls_dict, self.EXPLOSIVE_CLASSES
        )
        monster_parts = {key: item for key, item in items.items() if "fake" not in key}
        return set(monster_parts.keys()), monster_parts

    def _get_monster_parts(self, results, grouped_by_cls_dict):
        items_keys, items = self._get_sections_by_class(
            results, grouped_by_cls_dict, {"II_ATTCH", "II_FOOD"}
        )
        monster_parts = {
            key: item
            for key, item in items.items()
            if item.get("monster_part") == "true" and key != "monster_part"
        }
        return set(monster_parts.keys()), monster_parts

    def _load_artefacts(self, sections: dict[str, dict]) -> None:
        cocoons = {
            section_name: section
            for section_name, section in sections.items()
            if section.get("cocoon", None) == "true" and section_name != "cocoon"
        }

        caps_anom = {
            section_name: section
            for section_name, section in sections.items()
            if section.get("caps_anom", None) == "true" and section_name != "caps_anom"
        }

        true_arts = {
            section_name: section
            for section_name, section in sections.items()
            if section.get("caps_anom", None) is None
            and section.get("cocoon", None) is None
        }

        self._load_sections(cocoons, MonsterEmbrionResource())
        self._load_sections(caps_anom, CapsAnomResource())
        self._load_sections(true_arts, TrueArtefactResource())

    def _load_sections(
        self, sections: dict[str, dict], resource: BaseModelResource
    ) -> None:
        for section_name, section in sections.items():
            resource.create_instance_from_data(section_name, section)

    def _get_sections_by_class(
        self, results, grouped_by_cls_dict, classes: set[str]
    ) -> tuple[set[str], dict[str, dict]]:
        ammo_keys = set()
        for key in classes:
            ammo_keys |= set(grouped_by_cls_dict[key])
        ammo = {
            ammo_key: results[ammo_key]
            for ammo_key in ammo_keys
            if ammo_key not in classes
        }
        return ammo_keys, ammo

    def _load_icon_xml(self, files: list[Path], name: str, fixer: GSCXmlFixer) -> None:
        print(f"Start parsing {name=}")
        for file in files:
            print(f"\tstart {file}")
            fixed_file_path = fixer.fix(file)
            root_node = parse(fixed_file_path).getroot()
            image = None
            for child_node in root_node:
                if child_node.tag == "file_name":
                    image_file_path = (
                        settings.OP22_GAME_DATA_PATH
                        / "textures"
                        / (child_node.text + ".dds")
                    )
                    image = Image.open(image_file_path)
            if image is None:
                raise ValueError(f"No image in {file}")
            loader = IconLoader(image)
            loader.load_bulk(root_node)
            print(f"\tfinish {file}")
        print(f"Finish parsing {name=}")

    def _load_xml(
        self,
        files: list[Path],
        resource: BaseModelXmlLoader,
        name: str,
        fixer: GSCXmlFixer,
    ) -> None:
        print(f"Start parsing {name=}")
        for file in files:
            print(f"\tstart {file}")
            fixed_file_path = fixer.fix(file)
            root_node = parse(fixed_file_path).getroot()
            resource.load_bulk(root_node)
            print(f"\tfinish {file}")
        print(f"Finish parsing {name=}")

    def _get_paths_list(
        self, base_path: Path, files_str: str, extension: str
    ) -> list[Path]:
        files_names = [s.strip() for s in files_str.split(",")]
        return [base_path / f"{file}.{extension}" for file in files_names]
