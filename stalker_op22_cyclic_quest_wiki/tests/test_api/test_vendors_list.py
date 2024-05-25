from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from stalker_op22_cyclic_quest_wiki.models import (
    CycleTaskVendor,
    CyclicQuest,
    Translation,
)
from stalker_op22_cyclic_quest_wiki.models.cycle_tasks.cycle_task import QuestKinds
from stalker_op22_cyclic_quest_wiki.tests.utils import (
    FAKE_ICON_URL,
    clear_fake_icon,
    create_fake_icon,
)


class TestVendorList(TestCase):
    def setUp(self) -> None:
        self.vendor1 = CycleTaskVendor.objects.create(
            section_name="sidor",
            local_id=1,
            game_story_id=1,
            name_translation=Translation.objects.create(
                code="sidor",
                rus="sidor",
                eng="sidor",
                ukr="sidor",
                pln="sidor",
                fra="sidor",
            ),
            icon=create_fake_icon(),
            position=None,
        )

        self.vendor2 = CycleTaskVendor.objects.create(
            section_name="barmen",
            local_id=2,
            game_story_id=2,
            name_translation=Translation.objects.create(
                code="barmen",
                rus="barmen",
                eng="barmen",
                ukr="barmen",
                pln="barmen",
                fra="barmen",
            ),
            icon=create_fake_icon(),
            position=None,
        )
        self.vendor3 = CycleTaskVendor.objects.create(
            section_name="saharov",
            local_id=3,
            game_story_id=3,
            name_translation=Translation.objects.create(
                code="saharov",
                rus="saharov",
                eng="saharov",
                ukr="saharov",
                pln="saharov",
                fra="saharov",
            ),
            icon=create_fake_icon(),
            position=None,
        )
        CyclicQuest.objects.create(
            game_code="1",
            type=QuestKinds.FIND_ARTEFACT,
            prior=0,
            once=False,
            vendor=self.vendor2,
            text=Translation.objects.create(
                code="quest1",
                rus="quest1",
                eng="quest1",
                ukr="quest1",
                pln="quest1",
                fra="quest1",
            ),
        )
        CyclicQuest.objects.create(
            game_code="2",
            type=QuestKinds.FIND_ARTEFACT,
            prior=0,
            once=False,
            vendor=self.vendor2,
            text=Translation.objects.create(
                code="quest2",
                rus="quest2",
                eng="quest2",
                ukr="quest2",
                pln="quest2",
                fra="quest2",
            ),
        )
        CyclicQuest.objects.create(
            game_code="3",
            type=QuestKinds.CHAIN,
            prior=0,
            once=False,
            vendor=self.vendor3,
            text=Translation.objects.create(
                code="quest3",
                rus="quest3",
                eng="quest3",
                ukr="quest3",
                pln="quest3",
                fra="quest3",
            ),
        )

    def tearDown(self) -> None:
        clear_fake_icon()

    def test_get_vendors_list(self) -> None:
        client = Client()
        response = client.get(reverse("api:task_vendors"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        expected_data = [
            {
                "id": str(self.vendor1.id),
                "icon_url": FAKE_ICON_URL,
                "name": {
                    "rus": "sidor",
                    "eng": "sidor",
                    "ukr": "sidor",
                    "pln": "sidor",
                    "fra": "sidor",
                },
                "tasks_count": 0,
                "has_chain": False,
            },
            {
                "id": str(self.vendor2.id),
                "icon_url": FAKE_ICON_URL,
                "name": {
                    "rus": "barmen",
                    "eng": "barmen",
                    "ukr": "barmen",
                    "pln": "barmen",
                    "fra": "barmen",
                },
                "tasks_count": 2,
                "has_chain": False,
            },
            {
                "id": str(self.vendor3.id),
                "icon_url": FAKE_ICON_URL,
                "name": {
                    "rus": "saharov",
                    "eng": "saharov",
                    "ukr": "saharov",
                    "pln": "saharov",
                    "fra": "saharov",
                },
                "tasks_count": 1,
                "has_chain": True,
            },
        ]
        self.assertEqual(expected_data, data)
