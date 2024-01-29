from django.db import models

from game_parser.models import Translation


class Location(models.Model):
    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    game_id = models.CharField(null=False, max_length=3, verbose_name='Ид уровня') #id (01)
    game_code = models.CharField(null=False, max_length=255, verbose_name='Название уровня') # section name (level01)
    name = models.CharField(null=True, max_length=255, verbose_name='Код человекочитабельного названия') # L01_Escape

    name_translation = models.ForeignKey(Translation, null=True, verbose_name='Перевод названия', on_delete=models.SET_NULL)
    offset_str = models.CharField(null=True, max_length=255, verbose_name='Сдвиг на глобальной карте??')

    def __str__(self):
        return f'Локация {self.name_translation} ({self.game_code})'


class LocationMapInfo(models.Model):
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, null=False)
    texture_raw = models.CharField(max_length=255, null=True)
    bound_rect_raw = models.CharField(max_length=255, null=True)
    global_rect_raw = models.CharField(max_length=255, null=True)
    weathers = models.CharField(max_length=255, null=True)
    music_tracks = models.CharField(max_length=255, null=True)
    map_image = models.ImageField(null=True)
