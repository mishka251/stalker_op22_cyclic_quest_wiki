from django.contrib.admin import TabularInline
from polymorphic.admin import StackedPolymorphicInline

class ReadOnlyMixin:
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class ReadOnlyNestedTable(ReadOnlyMixin, TabularInline):
    pass

class ReadOnlyPolymorphicInline(ReadOnlyMixin, StackedPolymorphicInline):
    pass

class ReadOnlyPolymorphicChildInline(ReadOnlyMixin, StackedPolymorphicInline.Child):
    pass