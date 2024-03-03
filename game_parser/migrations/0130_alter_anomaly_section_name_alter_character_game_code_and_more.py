# Generated by Django 4.2 on 2024-02-29 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0129_alter_icon_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anomaly',
            name='section_name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='game_code',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='cycletaskvendor',
            name='game_story_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game_parser.gamestoryid', unique=True),
        ),
        migrations.AlterField(
            model_name='cycletaskvendor',
            name='game_story_id_raw',
            field=models.PositiveSmallIntegerField(unique=True, verbose_name='game id'),
        ),
        migrations.AlterField(
            model_name='cycletaskvendor',
            name='vendor_id',
            field=models.PositiveSmallIntegerField(unique=True, verbose_name='game id'),
        ),
        migrations.AlterField(
            model_name='cyclicquest',
            name='game_code',
            field=models.CharField(max_length=255, unique=True, verbose_name='Игровой код в файле'),
        ),
        migrations.AlterField(
            model_name='dialog',
            name='game_id',
            field=models.CharField(max_length=512, unique=True, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='gamestoryid',
            name='section_name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название секции'),
        ),
        migrations.AlterField(
            model_name='gamestoryid',
            name='story_id',
            field=models.PositiveSmallIntegerField(unique=True, verbose_name='id в игре'),
        ),
        migrations.AlterField(
            model_name='infoportion',
            name='game_id',
            field=models.CharField(max_length=512, unique=True, verbose_name='Игровой идентификатор'),
        ),
        migrations.AlterField(
            model_name='inventorybox',
            name='section_name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название секции'),
        ),
        migrations.AlterField(
            model_name='location',
            name='game_code',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название уровня'),
        ),
        migrations.AlterField(
            model_name='location',
            name='game_id',
            field=models.CharField(max_length=3, unique=True, verbose_name='Ид уровня'),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='Код человекочитабельного названия'),
        ),
        migrations.AlterField(
            model_name='monster',
            name='section_name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='questrandomreward',
            name='index',
            field=models.PositiveSmallIntegerField(null=True, unique=True, verbose_name='Индекс'),
        ),
        migrations.AlterField(
            model_name='questrandomreward',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Игровое название'),
        ),
        migrations.AlterField(
            model_name='recept',
            name='anomaly_id',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='trader',
            name='game_code',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='translation',
            name='code',
            field=models.CharField(max_length=128, unique=True, verbose_name='Код названия'),
        ),
        migrations.AlterUniqueTogether(
            name='itemintreasure',
            unique_together={('item', 'treasure')},
        ),
        migrations.AlterUniqueTogether(
            name='itemintreasurebox',
            unique_together={('item', 'box')},
        ),
    ]