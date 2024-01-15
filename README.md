# stalker_op22_cyclic_quest_wiki
Планируется создание сайта с информацией о циклических квестах в моде на игру сталкер Объединенный пак 2.2


## Примерные планы

1. Приблизительная структура моделей
2. Парсер `gamedata` ltx -> python class(без связей) -> django model(со связями)
3. API + фронт
4. публикация


Примерная структура `gamedata`

* [x] Квесты(ЦЗ) - `config/misc/cycle_task.ltx`
* [x] Оружие - почти вся папка `config/weapons` (файлы с префиксом w)
* [x] Гранаты - `config/weapons/grenade.ltx`
* [x] Патроны -  `config/weapons/ammo.ltx`
* [x] Обвесы - папка `config/weapons/arsenal_mod/addons`
* [x] Артефакты:
   * `config/misc/artefacts.ltx`
   * `config/misc/artefacts_amkzp.ltx`
   * `config/misc/embrions.ltx`
  
* [x] Медицина - `config/misc/items.ltx`
* [x] Части мутантов - `config/misc/monster_items.ltx`
* [x] Броня - `config/misc/outfit.ltx`
* [x] Прочее :
   * `config/misc/arc.ltx`
   * `config/misc/arhara_items.ltx`
   * `config/misc/devices.ltx`
   * `config/misc/items.ltx`
   * `config/misc/ogg_player.ltx`
   * `config/misc/pnv.ltx`
   * ...


Заметки
* [ ] тайники 
   * `config/misc/ph_box_generic.ltx`
   * `config/misc/ph_box_items_by_communities.ltx`
   * `config/misc/ph_box_items_by_levels.ltx`
   * `config/misc/ph_box_items_count.ltx`
   * `config/misc/treasure.ltx`

* [ ] Предметы у убитых сталкеров
   *  `config/misc/death_manager/by_communities.ltx`
   *  `config/misc/death_manager/by_levels.ltx`
   * `config/misc/death_manager/generic.ltx`

* [x] Торговцы `config/trade`

* [x] Переводы папка `config/text/*.xml`
   * `arsenal_mod.xml`
   * `artefacts.xml`
   * `cycle_task.xml`
   * `devices.xml`
   * `items.xml`
   * `outfit.xml`
   * `questman.xml`
   * `sak_strings.xml`
   * `weapons.xml`

* [x] Иконки `textures/ui/ui_icon_equipment.dds`





Идея: сделать 2 приложения с моделями для django
В одном - все поля необязательные и "не строгие".
Храним ссылки на другие объекты в двойном виде 1) ForeignKey, 2) текстом, чтобы не ломалось при отсутствии объекта

Во втором - уже с жесткими связями и обязательными полями. 

Ход работы: 
1. Парсингом ltx-файлов максимально заполнить первые модели
2. Руками поправить данные в БД по необходимости(или допилить парсер)
3. Перенести данные из 1 в 2


Правка по парсингу NPC/торговцев

1. Надо найти всех персонажей в spawn_sections `config/creatures/spawn_sections.ltx`
2. Найти у них `custom_data` и прочитать этот файл
3. Найти в custom_data секцию `logic` и в ней ключ `trade`
4. Прочитать файл trade


Пример для Ааза(reverse)
4. Торговля trade/aaz.ltx указано в `config/scripts/jupiter/jup_aaz_logic.ltx`
3. `config/scripts/jupiter/jup_aaz_logic.ltx` указано в `config/creatures/spawn_sections.ltx` в `aaz_upi_torg`
2. Там же в `aaz_upi_torg` указан профиль `aaz_upi`
1. Также профиль `aaz_upi` указан в `config/game_story_ids.ltx` для квестов


А как вытащить локации и расположение неписей на них??

Все Локации - `config/game_levels.ltx`
Игровая карта - `config/game_maps_single.ltx`


Парсинг сюжетных квестов

Диалоги
* `config/gameplay/dialogss*.xml`
* `<action>` - название скрипта из файла в `scripts`
* По скриптам можно пройтись и увидеть что дают(по именам функций)






TODO

Распасить скрипты со спавном НПС, чтобы понять найти связь story_id и секции для динамически спавнящихся квестодателей

Например, Пропер 70 и Обитель зла:
story_id `19907`, `19903`, `19909`
Спавнятся в `scripts/snp.script` `scripts/snp.script:1164` `spawn_bunker_jupiter`
Секции `proper70_jupiter`, `resident_evil_jupiter`, `anna_jupiter`

Далее надо найти эти секции в `config/creatures/spawn_sections_snp.ltx` и распарсить из них `character_profile`


Спавн предметов в ящиках
`scripts/xr_box.script`

Спавн зависит от локации + группировки + сложности

Спавн по грппировке добавляется к локе и кастомным предметам(похоже)

