# Generated by Django 4.2 on 2024-02-13 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0123_alter_baseitem_options_alter_dialog_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskobjective',
            options={'verbose_name': 'Цель сюжетного задания', 'verbose_name_plural': 'Цели сюжетных заданий'},
        ),
        migrations.AddField(
            model_name='taskobjective',
            name='function_call_complete',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='call_on_complete_task_objective', to='game_parser.scriptfunction', verbose_name='Функция, вызываемая при завершении'),
        ),
        migrations.AddField(
            model_name='taskobjective',
            name='function_complete',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='on_complete_task_objective', to='game_parser.scriptfunction', verbose_name='Функция, вызываемая при завершении'),
        ),
        migrations.AddField(
            model_name='taskobjective',
            name='function_fail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='set_on_fail_task_objective', to='game_parser.scriptfunction', verbose_name='Функция, вызываемая при провале'),
        ),
        migrations.AddField(
            model_name='taskobjective',
            name='infoportion_complete',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='on_complete_task_objective', to='game_parser.infoportion', verbose_name='Инфопоршень, устанавлеваемый при завершении'),
        ),
        migrations.AddField(
            model_name='taskobjective',
            name='infoportion_set_complete',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='set_on_complete_task_objective', to='game_parser.infoportion', verbose_name='Инфопоршень, устанавлеваемый при завершении'),
        ),
        migrations.AddField(
            model_name='taskobjective',
            name='infoportion_set_fail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='set_on_fail_task_objective', to='game_parser.infoportion', verbose_name='Инфопоршень, устанавлеваемый при провале'),
        ),
        migrations.AlterField(
            model_name='taskobjective',
            name='function_call_complete_raw',
            field=models.TextField(null=True, verbose_name='Функция, вызываемая при завершении'),
        ),
        migrations.AlterField(
            model_name='taskobjective',
            name='function_complete_raw',
            field=models.TextField(null=True, verbose_name='Функция, вызываемая при завершении'),
        ),
        migrations.AlterField(
            model_name='taskobjective',
            name='function_fail_raw',
            field=models.TextField(null=True, verbose_name='Функция, вызываемая при провале'),
        ),
        migrations.AlterField(
            model_name='taskobjective',
            name='infoportion_complete_raw',
            field=models.TextField(null=True, verbose_name='Инфопоршень, устанавлеваемый при завершении'),
        ),
        migrations.AlterField(
            model_name='taskobjective',
            name='infoportion_set_complete_raw',
            field=models.TextField(null=True, verbose_name='Инфопоршень, устанавлеваемый при завершении'),
        ),
        migrations.AlterField(
            model_name='taskobjective',
            name='infoportion_set_fail_raw',
            field=models.TextField(null=True, verbose_name='Инфопоршень, устанавлеваемый при провале'),
        ),
    ]
