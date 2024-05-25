from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from stalker_op22_cyclic_quest_wiki.models import (
    CycleTaskTargetItem,
    CycleTaskVendor,
    CyclicQuest,
    Item,
    ItemReward,
    MoneyReward,
    Translation,
    TreasureReward,
)
from stalker_op22_cyclic_quest_wiki.models.cycle_tasks.cycle_task import QuestKinds
from stalker_op22_cyclic_quest_wiki.tests.utils import (
    clear_fake_icon,
    create_fake_icon,
    get_fake_icon_data,
)


def _create_fake_translation(code: str, rus: str | None = None) -> Translation:
    return Translation.objects.create(
        code=code,
        rus=rus or code,
        eng=rus or code,
        ukr=rus or code,
        pln=rus or code,
        fra=rus or code,
    )


class TestVendorList(TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.item1 = Item.objects.create(
            cost=100,
            name="ak",
            inv_weight=3,
            icon=create_fake_icon(),
            name_translation=_create_fake_translation("ak"),
            description_translation=_create_fake_translation("ak_desc"),
        )
        self.vendor = CycleTaskVendor.objects.create(
            section_name="sidor",
            local_id=1,
            game_story_id=1,
            name_translation=_create_fake_translation("sidor"),
            icon=create_fake_icon(),
            position=None,
        )

        quest1 = CyclicQuest.objects.create(
            game_code="1",
            type=QuestKinds.FIND_ARTEFACT,
            prior=0,
            once=False,
            vendor=self.vendor,
            text=_create_fake_translation(
                code="quest1",
            ),
        )
        CycleTaskTargetItem.objects.create(
            item=self.item1,
            count=1,
            cond_str="50",
            quest=quest1,
        )
        quest2 = CyclicQuest.objects.create(
            game_code="2",
            type=QuestKinds.FIND_ARTEFACT,
            prior=1,
            once=False,
            vendor=self.vendor,
            text=_create_fake_translation(
                code="quest2",
            ),
        )
        CycleTaskTargetItem.objects.create(
            item=self.item1,
            count=2,
            cond_str="10, 49.99",
            quest=quest2,
        )
        ItemReward.objects.create(
            item=self.item1,
            count=1,
            quest=quest2,
        )
        TreasureReward.objects.create(
            quest=quest2,
        )
        quest3 = CyclicQuest.objects.create(
            game_code="3",
            type=QuestKinds.CHAIN,
            prior=0,
            once=False,
            vendor=self.vendor,
            text=_create_fake_translation(
                code="quest3",
            ),
        )
        CycleTaskTargetItem.objects.create(
            item=self.item1,
            count=2,
            cond_str="10, 49.99",
            quest=quest3,
        )
        MoneyReward.objects.create(
            quest=quest3,
            money=1500,
        )

    def tearDown(self) -> None:
        clear_fake_icon()

    def test_get_vendors_quest(self) -> None:
        client = Client()
        response = client.get(
            reverse("api:vendor_tasks", kwargs={"vendor_id": self.vendor.id}),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        expexted_item_json = {
            "item_id": "ak",
            "item_label": "ak",
            "icon": get_fake_icon_data(),
        }
        expected_data = [
            {
                "kind": {"value": "artefact", "label": "Принести артефакт"},
                "prior": 0,
                "text": "quest1",
                "target": {
                    "_type": "item",
                    "item": expexted_item_json,
                    "items_count": 1,
                    "state": {
                        "min": 50.0,
                        "max": 100,
                    },
                },
                "rewards": [],
            },
            {
                "kind": {"value": "artefact", "label": "Принести артефакт"},
                "prior": 1,
                "text": "quest2",
                "target": {
                    "_type": "item",
                    "item": expexted_item_json,
                    "items_count": 2,
                    "state": {
                        "min": 10.0,
                        "max": 49.99,
                    },
                },
                "rewards": [
                    {
                        "_type": "item",
                        "count": 1,
                        "item": expexted_item_json,
                    },
                    {
                        "_type": "treasure",
                        "icon": None,
                    },
                ],
            },
            {
                "kind": {"value": "chain", "label": "Цепочка"},
                "prior": 0,
                "text": "quest3",
                "target": {
                    "_type": "item",
                    "item": expexted_item_json,
                    "items_count": 2,
                    "state": {
                        "min": 10.0,
                        "max": 49.99,
                    },
                },
                "rewards": [
                    {
                        "_type": "money",
                        "count": 1500,
                        "icon": None,
                    },
                ],
            },
        ]
        self.assertEqual(expected_data, data)
