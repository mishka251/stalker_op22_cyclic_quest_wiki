# Generated by Django 4.2 on 2023-04-13 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0075_alter_cyclicquestitemreward_quest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cyclicquestitemreward',
            options={'verbose_name': 'Предмет в награду за ЦЗ', 'verbose_name_plural': 'Предметы в наградах за ЦЗ'},
        ),
        migrations.AlterUniqueTogether(
            name='cyclicquestitemreward',
            unique_together={('item', 'quest'), ('raw_item', 'quest')},
        ),
    ]
