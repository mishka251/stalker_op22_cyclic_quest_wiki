import math
from http import HTTPStatus

from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse

from stalker_op22_cyclic_quest_wiki.models import CycleTaskVendor, Item


class TestAllViews(TestCase):
    """Smoke test на все возможные view с учётом данных в БД"""

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.client = Client()
        call_command("import_data", imported_archive="data/data.zip", skip_checks=True)

    def test_main(self) -> None:
        self._assert_view_working(reverse("index"))

    def test_vendors_list(self) -> None:
        self._assert_view_working(reverse("task_vendors"))

    def test_items_list(self) -> None:
        items = Item.objects.count()
        pages = math.floor(items / 35)
        base_url = reverse("items")
        for page_number in range(1, pages):
            with self.subTest(f"{page_number=}"):
                self._assert_view_working(base_url + f"?page={page_number}")

    def test_vendor_quests(self) -> None:
        for vendor in CycleTaskVendor.objects.all():
            with self.subTest(f"{vendor=}"):
                base_url = reverse("vendor_tasks", kwargs={"vendor_id": vendor.id})
                self._assert_view_working(base_url)

    def test_where_item_needed(self) -> None:
        for item in Item.objects.all():
            with self.subTest(f"{item=}"):
                base_url = reverse("where_item_needed", kwargs={"item_id": item.id})
                self._assert_view_working(base_url)

    def test_where_find_item(self) -> None:
        for item in Item.objects.all():
            with self.subTest(f"{item=}"):
                base_url = reverse("where_find_item", kwargs={"item_id": item.id})
                self._assert_view_working(base_url)

    def test_api_vendors_list(self) -> None:
        self._assert_view_working(reverse("api:task_vendors"))

    def test_api_items_list(self) -> None:
        items = Item.objects.count()
        pages = math.ceil(items / 35)
        base_url = reverse("api:items")
        for page_number in range(1, pages):
            with self.subTest(f"{page_number=}"):
                self._assert_view_working(base_url + f"?page={page_number}")

    def test_api_vendor_quests(self) -> None:
        for vendor in CycleTaskVendor.objects.all():
            with self.subTest(f"{vendor=}"):
                base_url = reverse("api:vendor_tasks", kwargs={"vendor_id": vendor.id})
                self._assert_view_working(base_url)

    def test_api_where_item_needed(self) -> None:
        for item in Item.objects.all():
            with self.subTest(f"{item=}"):
                base_url = reverse("api:where_need_item", kwargs={"item_id": item.id})
                self._assert_view_working(base_url)

    def test_api_where_find_item(self) -> None:
        for item in Item.objects.all():
            with self.subTest(f"{item=}"):
                base_url = reverse("api:where_find_item", kwargs={"item_id": item.id})
                self._assert_view_working(base_url)

    def _assert_view_working(self, url: str) -> None:
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
