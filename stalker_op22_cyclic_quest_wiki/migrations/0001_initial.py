# Generated by Django 4.2.11 on 2024-04-09 21:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="CycleTaskVendor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("section_name", models.CharField(max_length=128, unique=True, verbose_name="Название секции НПС")),
                ("local_id", models.PositiveSmallIntegerField(unique=True, verbose_name="ID квестодателя локальный(в cycle_task.ltx)")),
                ("game_story_id", models.PositiveSmallIntegerField(unique=True, verbose_name="ID квестодателя глобальный(story_id)")),
            ],
            options={
                "verbose_name": "Квестодатель",
                "verbose_name_plural": "Квестодатели",
            },
        ),
        migrations.CreateModel(
            name="Icon",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=512, unique=True)),
                ("icon", models.ImageField(upload_to="")),
            ],
            options={
                "verbose_name": "Иконка",
                "verbose_name_plural": "Иконки",
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("cost", models.PositiveIntegerField(verbose_name="Базовая цена")),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="Название(код в игре)")),
                ("inv_weight", models.DecimalField(decimal_places=3, max_digits=12, verbose_name="Вес")),
            ],
            options={
                "verbose_name": "Предмет",
                "verbose_name_plural": "Предметы",
            },
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, unique=True)),
                ("offset_str", models.CharField(max_length=255, null=True, verbose_name="Сдвиг на глобальной карте??")),
                ("global_rect_raw", models.CharField(max_length=255, null=True, verbose_name="Границы локации(относительно глобальной карты?)")),
            ],
            options={
                "verbose_name": "Локация",
                "verbose_name_plural": "Локации",
            },
        ),
        migrations.CreateModel(
            name="LocationMapInfo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("location_name", models.CharField(max_length=255, unique=True)),
                ("map_image", models.ImageField(upload_to="", verbose_name="Карта")),
                ("bound_rect_raw", models.CharField(max_length=255, verbose_name="Границы локации(границы картинки?)")),
                ("min_x", models.FloatField()),
                ("max_x", models.FloatField()),
                ("min_y", models.FloatField()),
                ("max_y", models.FloatField()),
            ],
            options={
                "verbose_name": "Карта локации",
                "verbose_name_plural": "Карты локации",
            },
        ),
        migrations.CreateModel(
            name="Translation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=128, unique=True, verbose_name="Код названия")),
                ("rus", models.TextField(verbose_name="Русский")),
                ("eng", models.TextField(verbose_name="Английский")),
                ("ukr", models.TextField(verbose_name="Украинский")),
                ("pln", models.TextField(verbose_name="Польский")),
                ("fra", models.TextField(verbose_name="Французский")),
            ],
            options={
                "verbose_name": "Перевод",
                "verbose_name_plural": "Переводы",
            },
        ),
        migrations.CreateModel(
            name="Ammo",
            fields=[
                ("item_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="stalker_op22_cyclic_quest_wiki.item")),
                ("box_size", models.PositiveIntegerField(verbose_name="Кол-во патронов в пачке?")),
            ],
            options={
                "verbose_name": "Боеприпас",
                "verbose_name_plural": "Боеприпасы",
            },
            bases=("stalker_op22_cyclic_quest_wiki.item",),
        ),
        migrations.CreateModel(
            name="StalkerRank",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=128, unique=True, verbose_name="Код")),
                ("translation", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="stalker_op22_cyclic_quest_wiki.translation", verbose_name="Название")),
            ],
            options={
                "verbose_name": "Ранг сталкера",
                "verbose_name_plural": "Ранги сталкеров",
            },
        ),
        migrations.CreateModel(
            name="RandomRewardInfo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("index", models.IntegerField(unique=True, verbose_name="Индекс")),
                ("description", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="stalker_op22_cyclic_quest_wiki.translation", verbose_name="Описание")),
                ("icon", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="stalker_op22_cyclic_quest_wiki.icon", verbose_name="Иконка")),
                ("possible_items", models.ManyToManyField(to="stalker_op22_cyclic_quest_wiki.item", verbose_name="Возможные предметы")),
            ],
            options={
                "verbose_name": "Описание случайной награды",
                "verbose_name_plural": "Описание случайных наград",
            },
        ),
        migrations.CreateModel(
            name="MapPosition",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="Название")),
                ("x", models.FloatField()),
                ("y", models.FloatField()),
                ("z", models.FloatField()),
                ("spawn_id", models.PositiveBigIntegerField(unique=True, verbose_name="ID")),
                ("story_id", models.PositiveBigIntegerField(null=True, unique=True, verbose_name="story_id")),
                ("spawn_story_id", models.PositiveBigIntegerField(null=True, unique=True, verbose_name="spawn_story_id")),
                ("game_vertex_id", models.PositiveBigIntegerField(verbose_name="vertexID")),
                ("location", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="stalker_op22_cyclic_quest_wiki.location")),
            ],
            options={
                "verbose_name": "Точка на локации",
                "verbose_name_plural": "Точки на локации",
            },
        ),
        migrations.AddField(
            model_name="location",
            name="map_info",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to="stalker_op22_cyclic_quest_wiki.locationmapinfo"),
        ),
        migrations.AddField(
            model_name="location",
            name="name_translation",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="stalker_op22_cyclic_quest_wiki.translation", verbose_name="Перевод названия"),
        ),
        migrations.AddField(
            model_name="item",
            name="description_translation",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="+", to="stalker_op22_cyclic_quest_wiki.translation", verbose_name="Перевод описания"),
        ),
        migrations.AddField(
            model_name="item",
            name="icon",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="stalker_op22_cyclic_quest_wiki.icon"),
        ),
        migrations.AddField(
            model_name="item",
            name="name_translation",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="+", to="stalker_op22_cyclic_quest_wiki.translation", verbose_name="Перевод названия"),
        ),
        migrations.AddField(
            model_name="item",
            name="polymorphic_ctype",
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="polymorphic_%(app_label)s.%(class)s_set+", to="contenttypes.contenttype"),
        ),
        migrations.CreateModel(
            name="CyclicQuest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("game_code", models.CharField(max_length=255, unique=True, verbose_name="Игровой код в файле")),
                ("type", models.CharField(choices=[("eliminate_lager", "Уничтожить лагерь"), ("chain", "Цепочка"), ("kill_stalker", "Убить сталкера"), ("monster_part", "Часть мутанта"), ("artefact", "Принести артефакт"), ("find_item", "Принести предмет"), ("defend_lager", "Защитить лагерь")], max_length=255, verbose_name="Тип задания(тип цели задания)")),
                ("prior", models.IntegerField(default=0, verbose_name=" Типа очередность задания")),
                ("once", models.BooleanField(default=False, verbose_name="Одноразовый ли квест")),
                ("text", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="+", to="stalker_op22_cyclic_quest_wiki.translation", verbose_name="Текст задания")),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="stalker_op22_cyclic_quest_wiki.cycletaskvendor", verbose_name="Кквестодатель")),
            ],
            options={
                "verbose_name": "Циклический квест",
                "verbose_name_plural": "Циклические квесты",
            },
        ),
        migrations.AddField(
            model_name="cycletaskvendor",
            name="icon",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="stalker_op22_cyclic_quest_wiki.icon", verbose_name="Фото НПС"),
        ),
        migrations.AddField(
            model_name="cycletaskvendor",
            name="name_translation",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="stalker_op22_cyclic_quest_wiki.translation", verbose_name="Имя НПС"),
        ),
        migrations.CreateModel(
            name="CycleTaskTarget",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("polymorphic_ctype", models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="polymorphic_%(app_label)s.%(class)s_set+", to="contenttypes.contenttype")),
                ("quest", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="stalker_op22_cyclic_quest_wiki.cyclicquest", unique=True, verbose_name="ЦЗ")),
            ],
            options={
                "verbose_name": "Цель ЦЗ",
                "verbose_name_plural": "Цели ЦЗ",
            },
        ),
        migrations.CreateModel(
            name="Community",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=128, unique=True, verbose_name="Код")),
                ("translation", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="stalker_op22_cyclic_quest_wiki.translation", verbose_name="Название")),
            ],
            options={
                "verbose_name": "Группировка",
                "verbose_name_plural": "Группировки",
            },
        ),
        migrations.CreateModel(
            name="TreasureReward",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("polymorphic_ctype", models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="polymorphic_%(app_label)s.%(class)s_set+", to="contenttypes.contenttype")),
                ("quest", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="stalker_op22_cyclic_quest_wiki.cyclicquest", verbose_name="ЦЗ")),
            ],
            options={
                "verbose_name": "Тайник в награду за ЦЗ",
                "verbose_name_plural": "Тайники в награду за ЦЗ",
                "unique_together": {("quest",)},
            },
        ),
        migrations.CreateModel(
            name="QuestRandomReward",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("count", models.PositiveIntegerField(default=1, verbose_name="Количество")),
                ("polymorphic_ctype", models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="polymorphic_%(app_label)s.%(class)s_set+", to="contenttypes.contenttype")),
                ("quest", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="stalker_op22_cyclic_quest_wiki.cyclicquest", verbose_name="ЦЗ")),
                ("reward", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="stalker_op22_cyclic_quest_wiki.randomrewardinfo", verbose_name="Описание случайной награды")),
            ],
            options={
                "verbose_name": "Случайная награда за ЦЗ",
                "verbose_name_plural": "Случайная награда за ЦЗ",
                "unique_together": {("reward", "quest")},
            },
        ),
        migrations.CreateModel(
            name="MoneyReward",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("money", models.PositiveIntegerField(verbose_name="Сумма")),
                ("polymorphic_ctype", models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="polymorphic_%(app_label)s.%(class)s_set+", to="contenttypes.contenttype")),
                ("quest", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="stalker_op22_cyclic_quest_wiki.cyclicquest", verbose_name="ЦЗ")),
            ],
            options={
                "verbose_name": "Деньги за ЦЗ",
                "verbose_name_plural": "Деньги за ЦЗ",
                "unique_together": {("quest",)},
            },
        ),
        migrations.CreateModel(
            name="ItemReward",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("count", models.PositiveIntegerField(default=1, verbose_name="Кол-во предметов")),
                ("item", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="stalker_op22_cyclic_quest_wiki.item", verbose_name="Предмет")),
                ("polymorphic_ctype", models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="polymorphic_%(app_label)s.%(class)s_set+", to="contenttypes.contenttype")),
                ("quest", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="stalker_op22_cyclic_quest_wiki.cyclicquest", verbose_name="ЦЗ")),
            ],
            options={
                "verbose_name": "Предмет за ЦЗ",
                "verbose_name_plural": "Предметы за ЦЗ",
                "unique_together": {("item", "quest")},
            },
        ),
        migrations.CreateModel(
            name="CycleTaskTargetStalker",
            fields=[
                ("cycletasktarget_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="stalker_op22_cyclic_quest_wiki.cycletasktarget")),
                ("community", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="stalker_op22_cyclic_quest_wiki.community", verbose_name="группа сталкера")),
                ("map_positions", models.ManyToManyField(to="stalker_op22_cyclic_quest_wiki.mapposition", verbose_name="Возможные места спавна")),
                ("rank", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="stalker_op22_cyclic_quest_wiki.stalkerrank", verbose_name="Ранг сталкера")),
            ],
            options={
                "verbose_name": "Сталкер цель ЦЗ",
                "verbose_name_plural": "Сталкеры цель ЦЗ",
            },
            bases=("stalker_op22_cyclic_quest_wiki.cycletasktarget",),
        ),
        migrations.CreateModel(
            name="CycleTaskTargetItem",
            fields=[
                ("cycletasktarget_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="stalker_op22_cyclic_quest_wiki.cycletasktarget")),
                ("count", models.PositiveIntegerField(null=True, verbose_name="Кол-во нужных предметов")),
                ("cond_str", models.CharField(max_length=255, null=True, verbose_name="Цель: состояние предмета ")),
                ("item", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="quests_when_needed", to="stalker_op22_cyclic_quest_wiki.item", verbose_name="Целевой предмет")),
            ],
            options={
                "verbose_name": "Предмет - цель ЦЗ",
                "verbose_name_plural": "Предметы - цели ЦЗ",
            },
            bases=("stalker_op22_cyclic_quest_wiki.cycletasktarget",),
        ),
        migrations.CreateModel(
            name="CycleTaskTargetCamp",
            fields=[
                ("cycletasktarget_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="stalker_op22_cyclic_quest_wiki.cycletasktarget")),
                ("communities", models.ManyToManyField(to="stalker_op22_cyclic_quest_wiki.community", verbose_name="Группы в лагере")),
                ("map_position", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="stalker_op22_cyclic_quest_wiki.mapposition", verbose_name="Место на карте")),
            ],
            options={
                "verbose_name": "Лагерь - цель ЦЗ",
                "verbose_name_plural": "Лагеря - цели ЦЗ",
            },
            bases=("stalker_op22_cyclic_quest_wiki.cycletasktarget",),
        ),
    ]
