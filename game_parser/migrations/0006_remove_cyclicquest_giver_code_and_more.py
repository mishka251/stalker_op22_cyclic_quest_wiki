# Generated by Django 4.1.3 on 2022-12-02 20:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0005_cyclicquest_defend_target_str_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cyclicquest',
            name='giver_code',
        ),
        migrations.AddField(
            model_name='cyclicquest',
            name='giver_code_global',
            field=models.CharField(max_length=255, null=True, verbose_name='Код квестодателя(глобальный)'),
        ),
        migrations.AddField(
            model_name='cyclicquest',
            name='giver_code_local',
            field=models.CharField(max_length=255, null=True, verbose_name='Код квестодателя(локальный)'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='condlist_str',
            field=models.CharField(max_length=1000, null=True, verbose_name='Условия для возможности получения задания'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='defend_target_str',
            field=models.CharField(max_length=255, null=True, verbose_name='Цель. Защита(?)'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='game_code',
            field=models.CharField(max_length=255, verbose_name='Игровой код в файле'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='giver',
            field=models.ForeignKey(max_length=255, null=True, on_delete=django.db.models.deletion.SET_NULL, to='game_parser.character', verbose_name='Персонаж квестодатель'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='hide_reward',
            field=models.BooleanField(default=False, verbose_name='Скрытая ли награда'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='map_location',
            field=models.CharField(max_length=255, null=True, verbose_name='Цель: на карте'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='once',
            field=models.BooleanField(default=False, verbose_name='Одноразовый ли квест'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='prior',
            field=models.IntegerField(default=0, verbose_name=' Типа очередность задания'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='random_rewards_string',
            field=models.CharField(max_length=255, null=True, verbose_name='Награда. Случайная'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='reward_dialog_str',
            field=models.CharField(max_length=512, null=True, verbose_name='Награда. Диалог(?)'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='reward_info_string',
            field=models.CharField(max_length=255, null=True, verbose_name='Награда. Информация'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='reward_item_string',
            field=models.CharField(max_length=255, null=True, verbose_name='Награда. Предметы(-ы)'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='reward_money',
            field=models.PositiveIntegerField(null=True, verbose_name='Награда. Деньги'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='reward_relation_str',
            field=models.CharField(max_length=255, null=True, verbose_name='Награда. Репутация/отношения'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='reward_treasure',
            field=models.BooleanField(default=False, verbose_name='Награда. Тайник'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='target_cond_str',
            field=models.CharField(max_length=255, null=True, verbose_name='Цель: состояние премдмета '),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='target_count',
            field=models.PositiveIntegerField(null=True, verbose_name='Кол-во нужных предметов'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='target_str',
            field=models.CharField(max_length=255, null=True, verbose_name='Цель задания'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='type',
            field=models.CharField(choices=[('eliminate_lager', 'Уничтожить лагерь'), ('chain', 'Цепочка'), ('kill_stalker', 'Убить'), ('monster_part', 'Часть мутанта'), ('artefact', 'Принести артефакт'), ('find_item', 'Принести предмет'), ('defend_lager', 'Защитить лагерь')], max_length=255, verbose_name='Тип задания(тип цели задания)'),
        ),
    ]
