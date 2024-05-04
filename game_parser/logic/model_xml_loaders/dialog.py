from django.db import IntegrityError
from lxml.etree import _Comment, _Element

from game_parser.logic.model_xml_loaders.base import BaseModelXmlLoader
from game_parser.models import Dialog, DialogPhrase


class DialogLoader(BaseModelXmlLoader[Dialog]):
    expected_tag = "dialog"

    def load_bulk(self, root_node: _Element) -> list[Dialog]:
        if root_node.tag == "game_dialogs":
            return super().load_bulk(root_node)
        results = []
        for game_dialogs in root_node:
            if game_dialogs.tag == "game_dialogs":
                results += super().load_bulk(root_node)
            else:
                raise ValueError(f"Unexpected node {game_dialogs.tag}")
        return results

    def _load(self, dialog_node: _Element, dialog_comments: list[str]) -> Dialog:
        if dialog_node.tag != "dialog":
            raise ValueError(f"Unexpected node {dialog_node.tag}")
        dialog_id = dialog_node.attrib.pop("id", "None")
        if dialog_id == "None":
            raise ValueError(f"Unexpected id is None {dialog_node}")
        dialog = Dialog.objects.create(
            game_id=dialog_id,
            comments_raw=";".join(dialog_comments),
        )
        preconditions = []
        has_info = []
        dont_has_info = []
        init_func = []
        for child_node in dialog_node:
            if child_node.tag == "precondition" and child_node.text:
                preconditions.append(child_node.text)
            elif child_node.tag == "has_info" and child_node.text:
                has_info.append(child_node.text)
            elif child_node.tag == "dont_has_info" and child_node.text:
                dont_has_info.append(child_node.text)
            elif child_node.tag == "init_func" and child_node.text:
                init_func.append(child_node.text)
            elif child_node.tag == "phrase_list" and child_node.text:
                self._parse_phrase_list(dialog, child_node)
            elif isinstance(child_node, _Comment):
                pass
            else:
                raise ValueError(
                    f"Unexpected game dialog child {child_node.tag} in {dialog_id}",
                )
        dialog.precondition_raw = ";".join(preconditions)
        dialog.dont_has_info_raw = ";".join(dont_has_info)
        dialog.has_info_raw = ";".join(has_info)
        dialog.init_func_raw = ";".join(init_func)
        dialog.save()
        return dialog

    def _parse_phrase_list(self, dialog: Dialog, phrase_list_node: _Element) -> None:
        for phrase_node in phrase_list_node:
            if phrase_node.tag == "phrase":
                phrase_id = phrase_node.attrib.pop("id")
                try:
                    phrase = DialogPhrase.objects.create(
                        dialog=dialog,
                        local_id=phrase_id,
                    )
                except IntegrityError as ex:
                    raise IntegrityError(f"{dialog=}, {phrase_id=}") from ex
                _next: list[str] = []
                precondition: list[str] = []
                action: list[str] = []
                give_info: list[str] = []
                dont_has_info: list[str] = []
                has_info: list[str] = []
                disable_info: list[str] = []
                disable: list[str] = []
                text = None
                for child_node in phrase_node:
                    if child_node.tag == "next" and child_node.text:
                        _next.append(child_node.text)
                    elif child_node.tag == "text" and child_node.text:
                        text = child_node.text
                    elif child_node.tag == "precondition" and child_node.text:
                        precondition.append(child_node.text)
                    elif child_node.tag == "action" and child_node.text:
                        action.append(child_node.text)
                    elif child_node.tag == "give_info" and child_node.text:
                        give_info.append(child_node.text)
                    elif child_node.tag == "dont_has_info" and child_node.text:
                        dont_has_info.append(child_node.text)
                    elif child_node.tag == "has_info" and child_node.text:
                        has_info.append(child_node.text)
                    elif child_node.tag == "disable_info" and child_node.text:
                        disable_info.append(child_node.text)
                    elif child_node.tag == "disable" and child_node.text:
                        disable.append(child_node.text)
                    elif isinstance(child_node, _Comment):
                        pass  # dialog_comments.append(game_dialogs.text)
                    else:
                        raise ValueError(
                            f"Unexpected dialog phrase child {child_node.tag} in {dialog.game_id} {phrase_id}",
                        )
                phrase.text_id_raw = text
                phrase.next_ids_raw = ";".join(_next)
                phrase.actions_raw = ";".join(action)
                phrase.precondition_raw = ";".join(precondition)
                phrase.give_info_raw = ";".join(give_info)
                phrase.has_info_raw = ";".join(has_info)
                phrase.dont_has_info_raw = ";".join(dont_has_info)
                phrase.disable_info_raw = ";".join(disable_info)
                phrase.disable_raw = ";".join(disable)
                phrase.save()
