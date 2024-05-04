import logging

from lxml.etree import _Comment, _Element

from game_parser.logic.model_xml_loaders.base import BaseModelXmlLoader
from game_parser.models import StorylineCharacter

logger = logging.getLogger(__name__)


class StorylineCharacterLoader(BaseModelXmlLoader[StorylineCharacter]):
    expected_tag = "specific_character"

    def _load(
        self,
        character_node: _Element,
        comments: list[str],
    ) -> StorylineCharacter:
        if character_node.tag != "specific_character":
            logger.warning("Unexpected node %s", character_node.tag)
            raise ValueError
        character_id = character_node.attrib.pop("id")
        character_no_random = bool(character_node.attrib.get("no_random"))
        name: str | None = None
        icon_raw: str | None = None
        community_raw = None
        dialogs_raw = []
        rank = None
        reputation = None
        start_dialog = None
        visual = None
        supplies_raw = None
        class_raw: str | None = None
        crouch_type_raw = None
        snd_config_raw = None
        money_min_raw = None
        money_max_raw = None
        money_inf_raw = None
        terrain_sect_raw = None
        bio_raw = None
        team = None
        for child_node in character_node:
            if child_node.tag == "name" and child_node.text is not None:
                name = child_node.text
            elif child_node.tag == "icon" and child_node.text is not None:
                icon_raw = child_node.text
            elif child_node.tag == "terrain_sect" and child_node.text is not None:
                terrain_sect_raw = child_node.text
            elif child_node.tag == "bio" and child_node.text is not None:
                bio_raw = child_node.text
            elif child_node.tag == "crouch_type" and child_node.text is not None:
                crouch_type_raw = child_node.text
            elif child_node.tag == "snd_config" and child_node.text is not None:
                snd_config_raw = child_node.text
            elif child_node.tag == "money":
                money_min_raw = child_node.attrib.pop("min")
                money_max_raw = child_node.attrib.pop("max")
                money_inf_raw = child_node.attrib.pop("infinitive")
            elif child_node.tag == "visual" and child_node.text is not None:
                visual = child_node.text
            elif child_node.tag == "class" and child_node.text is not None:
                class_raw = child_node.text
            elif child_node.tag == "supplies" and child_node.text is not None:
                supplies_raw = child_node.text
            elif child_node.tag == "rank" and child_node.text is not None:
                rank = int(child_node.text)
            elif child_node.tag == "reputation" and child_node.text is not None:
                reputation = int(child_node.text)
            elif child_node.tag == "community" and child_node.text is not None:
                community_raw = child_node.text
            elif child_node.tag == "actor_dialog" and child_node.text is not None:
                dialogs_raw.append(child_node.text)
            elif child_node.tag == "start_dialog" and child_node.text is not None:
                start_dialog = child_node.text
            elif isinstance(child_node, _Comment) or child_node.tag in {
                "panic_threshold",
                "panic_treshold",
                "map_icon",
            }:  # WTF misstype??
                pass
            elif child_node.tag == "team":
                team = child_node.text
            else:
                logger.warning(
                    "Unexpected node %s in character %s",
                    child_node.tag,
                    character_id,
                )

        if name is None or icon_raw is None or class_raw is None:
            raise TypeError
        return StorylineCharacter.objects.create(
            game_code=character_id,
            game_id=character_id,
            name=name,
            name_raw=name,
            comments=";".join(comments),
            icon_raw=icon_raw,
            community_default_raw=community_raw,
            dialogs_raw=";".join(dialogs_raw),
            rank=rank,
            reputation=reputation,
            start_dialog_row=start_dialog,
            no_random=character_no_random,
            visual_raw=visual,
            supplies_raw=supplies_raw,
            class_raw=class_raw,
            crouch_type_raw=crouch_type_raw,
            snd_config_raw=snd_config_raw,
            money_min_raw=money_min_raw,
            money_max_raw=money_max_raw,
            money_inf_raw=money_inf_raw,
            terrain_sect_raw=terrain_sect_raw,
            bio_raw=bio_raw,
            team_raw=team,
        )
