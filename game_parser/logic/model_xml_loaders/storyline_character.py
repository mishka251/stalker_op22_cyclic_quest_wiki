import logging

from lxml.etree import Element, _Comment

from game_parser.logic.model_xml_loaders.base import BaseModelXmlLoader
from game_parser.models import StorylineCharacter

logger = logging.getLogger(__name__)


class StorylineCharacterLoader(BaseModelXmlLoader[StorylineCharacter]):
    expected_tag = "specific_character"

    def _load(self, character_node: Element, comments: list[str]) -> StorylineCharacter:
        if character_node.tag != "specific_character":
            logger.warning("Unexpected node %s", character_node.tag)
            raise ValueError
        character_id = character_node.attrib.pop("id")
        character_no_random = bool(character_node.attrib.pop("no_random", None))
        name = None
        icon_raw = None
        community_raw = None
        dialogs_raw = []
        rank = None
        reputation = None
        start_dialog = None
        visual = None
        supplies_raw = None
        class_raw = None
        crouch_type_raw = None
        snd_config_raw = None
        money_min_raw = None
        money_max_raw = None
        money_inf_raw = None
        terrain_sect_raw = None
        bio_raw = None
        team = None
        for child_node in character_node:
            if child_node.tag == "name":
                name = child_node.text
            elif child_node.tag == "icon":
                icon_raw = child_node.text
            elif child_node.tag == "terrain_sect":
                terrain_sect_raw = child_node.text
            elif child_node.tag == "bio":
                bio_raw = child_node.text
            elif child_node.tag == "crouch_type":
                crouch_type_raw = child_node.text
            elif child_node.tag == "snd_config":
                snd_config_raw = child_node.text
            elif child_node.tag == "money":
                money_min_raw = child_node.attrib.pop("min")
                money_max_raw = child_node.attrib.pop("max")
                money_inf_raw = child_node.attrib.pop("infinitive")
            elif child_node.tag == "visual":
                visual = child_node.text
            elif child_node.tag == "class":
                class_raw = child_node.text
            elif child_node.tag == "supplies":
                supplies_raw = child_node.text
            elif child_node.tag == "rank":
                rank = int(child_node.text)
            elif child_node.tag == "reputation":
                reputation = int(child_node.text)
            elif child_node.tag == "community":
                community_raw = child_node.text
            elif child_node.tag == "actor_dialog":
                dialogs_raw.append(child_node.text)
            elif child_node.tag == "start_dialog":
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
                    f"Unexpected node %s in character %s", child_node.tag, character_id
                )
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
