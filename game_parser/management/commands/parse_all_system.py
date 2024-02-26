import logging
from itertools import groupby
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from lxml.etree import parse
from PIL import Image

from game_parser.logic.gsc_xml_fixer import GSCXmlFixer
from game_parser.logic.ltx_parser import LtxParser
from game_parser.logic.model_xml_loaders.base import BaseModelXmlLoader
from game_parser.logic.model_xml_loaders.dialog import DialogLoader
from game_parser.logic.model_xml_loaders.encyclopedia import EncyclopediaArticleLoader
from game_parser.logic.model_xml_loaders.icon import IconLoader
from game_parser.logic.model_xml_loaders.infoportion import InfoPortionLoader
from game_parser.logic.model_xml_loaders.storyline_character import StorylineCharacterLoader
from game_parser.logic.model_xml_loaders.translation import TranslationLoader
from game_parser.models import EncyclopediaGroup, EncyclopediaArticle

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    AMMO_CLASSES = {"AMMO"}
    ARTEFACT_classes = {"ARTEFACT"}
    GRENADE_AUNCHED_CLASSES = {
        "A_M209",
        "A_OG7B",
        "A_VOG25"
    }

    HANDLE_GRENADES_CLASSES = {
        "G_F1",
        "G_FAKE",
        "G_RGD5",
        "G_RPG7",
    }

    MEDICINE_CLASSES = {
        "II_ANTIR",
        "II_ATTCH",
        "II_BANDG",
        "II_BOLT",
        "II_BOTTL",
        "II_DOC",
        "II_EXPLO",
        "II_FOOD",
        "II_MEDKI",
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
    }

    WEAPON_CLASSES = {
        "WP_AK74",
        "WP_BINOC",
        "WP_BM16",
        "WP_GROZA",
        "WP_HPSA",
        "WP_KNIFE",
        "WP_LR300",
        "WP_PM",
        "WP_RG6",
        "WP_RPG7",
        "WP_SCOPE",
        "WP_SHOTG",
        "WP_SVD",
        "WP_SVU",
        "WP_USP45",
        "WP_VAL",
        "WP_VINT",
        "WP_WALTH",
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

    @atomic
    def handle(self, **options):
        base_path = settings.OP22_GAME_DATA_PATH
        system_file = base_path / "config" / "system.ltx"
        known_bases = {}
        EncyclopediaGroup.objects.all().delete()
        EncyclopediaArticle.objects.all().delete()

        parser = LtxParser(system_file, known_extends=known_bases)
        results = parser.get_parsed_blocks()

        translation_config = results["string_table"]
        translation_files_sources = self._get_paths_list(base_path / "config" / "text", translation_config["files"],
                                                         "xml")

        print("TRANSLATION", all(p.exists() for p in translation_files_sources), *translation_files_sources, sep='\n',
              end="\n" * 3)

        texture_desc_config = results["texture_desc"]
        texture_desc_sources = self._get_paths_list(base_path / "config" / "ui", texture_desc_config["files"], "xml")
        print("TEXTURE", all(p.exists() for p in texture_desc_sources), *texture_desc_sources, sep='\n', end="\n" * 3)

        info_portions_config = results["info_portions"]
        info_portions_sources = self._get_paths_list(base_path / "config" / "gameplay", info_portions_config["files"],
                                                     "xml")
        print("INFO_PORTION", all(p.exists() for p in info_portions_sources), *info_portions_sources, sep='\n',
              end="\n" * 3)

        encyclopedia_config = results["encyclopedia"]
        encyclopedia_sources = self._get_paths_list(base_path / "config" / "gameplay", encyclopedia_config["files"],
                                                    "xml")
        print("ENCYCLOPEDIA", all(p.exists() for p in encyclopedia_sources), *encyclopedia_sources, sep='\n',
              end="\n" * 3)

        dialogs_config = results["dialogs"]
        dialogs_sources = self._get_paths_list(base_path / "config" / "gameplay", dialogs_config["files"], "xml")
        print("DIALOGS", all(p.exists() for p in dialogs_sources), *dialogs_sources, sep='\n', end="\n" * 3)

        profiles_config = results["profiles"]
        profiles_sources = self._get_paths_list(base_path / "config" / "gameplay", profiles_config["files"], "xml")
        print("PROFILES", all(p.exists() for p in profiles_sources), *profiles_sources, sep='\n', end="\n" * 3)

        specific_characters_sources = self._get_paths_list(base_path / "config" / "gameplay",
                                                           profiles_config["specific_characters_files"], "xml")
        print("SPECIFIC_CHARACTERS", all(p.exists() for p in specific_characters_sources), *specific_characters_sources,
              sep='\n', end="\n" * 3)

        existing_sections_keys = [k for k in results.keys() if isinstance(results[k], dict)]

        sorted_by_cls_ = sorted(existing_sections_keys, key=lambda key: results[key].get("class", "None"))
        for cls_, keys in groupby(sorted_by_cls_, key=lambda key: results[key].get("class", "None")):
            keys = list(keys)
            print(cls_, len(keys))

        # TODO Проверить все секции на то, что всё есть в БД
        results_lists_keys = [k for k in results.keys() if isinstance(results[k], list)]
        print("START FILLING")

        # for translation_files_source in translation_files_sources:
        self._load_xml(translation_files_sources, TranslationLoader(), "Translation", GSCXmlFixer(encoding="utf-8"))
        self._load_xml(info_portions_sources, InfoPortionLoader(), "Info", GSCXmlFixer())
        self._load_xml(encyclopedia_sources, EncyclopediaArticleLoader(), "ENCYCLOPEDIA", GSCXmlFixer())
        self._load_xml(dialogs_sources, DialogLoader(), "DIALOGS", GSCXmlFixer())
        # self._load_xml(profiles_sources, TranslationLoader(), "PROFILES")
        self._load_xml(specific_characters_sources, StorylineCharacterLoader(), "SPECIFIC_CHARACTERS", GSCXmlFixer())
        self._load_icon_xml(texture_desc_sources, "TEXTURE", GSCXmlFixer())

    def _load_icon_xml(self, files: list[Path], name: str, fixer: GSCXmlFixer) -> None:
        print(f"Start parsing {name=}")
        for file in files:
            print(f"\tstart {file}")
            fixed_file_path = fixer.fix(file)
            root_node = parse(fixed_file_path).getroot()
            image = None
            for child_node in root_node:
                if child_node.tag == 'file_name':
                    image_file_path = settings.OP22_GAME_DATA_PATH/'textures'/(child_node.text+'.dds')
                    image = Image.open(image_file_path)
            if image is None:
                raise ValueError(f"No image in {file}")
            loader = IconLoader(image)
            loader.load_bulk(root_node)
            print(f"\tfinish {file}")
        print(f"Finish parsing {name=}")

    def _load_xml(self, files: list[Path], resource: BaseModelXmlLoader, name: str, fixer: GSCXmlFixer) -> None:
        print(f"Start parsing {name=}")
        for file in files:
            print(f"\tstart {file}")
            fixed_file_path = fixer.fix(file)
            root_node = parse(fixed_file_path).getroot()
            resource.load_bulk(root_node)
            print(f"\tfinish {file}")
        print(f"Finish parsing {name=}")

    def _get_paths_list(self, base_path: Path, files_str: str, extension: str) -> list[Path]:
        files_names = [s.strip() for s in files_str.split(",")]
        paths = [base_path / f"{file}.{extension}" for file in files_names]
        return paths
