# stalker_op22_cyclic_quest_wiki
Планируется создание сайта с информацией о циклических квестах в моде на игру сталкер Объединенный пак 2.2


## Примерные планы

1. Приблизительная структура моделей
2. Парсер `damedata` ltx -> python class(без связей) -> django model(со связями)
3. API + фронт
4. публикация


Примерная структура `gamedata`

* Квесты(ЦЗ) - `config/misc/cycle_task.ltx`
* Оружие - почти вся папка `config/weapons` (файлы с префиксом w)
* Гранаты - `config/weapons/grenade.ltx`
* Патроны -  `config/weapons/ammo.ltx`
* Обвесы - папка `config/weapons/arsenal_mod/addons`
* Артефакты:
   * `config/misc/artefacts.ltx`
   * `config/misc/artefacts_amkzp.ltx`
   * `config/misc/embrions.ltx`
  
* Медицина - `config/misc/items.ltx`
* Части мутантов - `config/misc/monster_items.ltx`
* Броня - `config/misc/outfit.ltx`
* Прочее :
   * `config/misc/arc.ltx`
   * `config/misc/arhara_items.ltx`
   * `config/misc/devices.ltx`
   * `config/misc/items.ltx`
   * `config/misc/ogg_player.ltx`
   * `config/misc/pnv.ltx`
   * ...


Заметки
* тайники 
   * `config/misc/ph_box_generic.ltx`
   * `config/misc/ph_box_items_by_communities.ltx`
   * `config/misc/ph_box_items_by_levels.ltx`
   * `config/misc/ph_box_items_count.ltx`
   * `config/misc/treasure.ltx`

* Предметы у убитых сталкеров
   *  `config/misc/death_manager/by_communities.ltx`
   *  `config/misc/death_manager/by_levels.ltx`
   * `config/misc/death_manager/generic.ltx`

* Торговцы `config/trade`









Идея: сделать 2 приложения с моделями для django
В одном - все поля необязательные и "не строгие".
Храним ссылки на другие объекты в двойном виде 1) ForeignKey, 2) текстом, чтобы не ломалось при отсутствии объекта

Во втором - уже с жесткими связями и обязательными полями. 

Ход работы: 
1. Парсингом ltx-файлов максимально заполнить первые модели
2. Руками поправить данные в БД по необходимости(или допилить парсер)
3. Перенести данные из 1 в 2