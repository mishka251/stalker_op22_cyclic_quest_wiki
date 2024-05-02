from django.contrib.admin import TabularInline
from django.http import HttpRequest
from polymorphic.admin import StackedPolymorphicInline


class ReadOnlyMixin:
    show_change_link = True

    def has_add_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


class ReadOnlyNestedTable(ReadOnlyMixin, TabularInline):
    pass


class ReadOnlyPolymorphicInline(ReadOnlyMixin, StackedPolymorphicInline):
    pass


class ReadOnlyPolymorphicChildInline(ReadOnlyMixin, StackedPolymorphicInline.Child):
    pass
