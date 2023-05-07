# Generated by Django 4.2 on 2023-05-07 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0082_alter_baseitem_options_baseitem_polymorphic_ctype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cyclicquest',
            name='type',
            field=models.CharField(choices=[('eliminate_lager', 'Уничтожить лагерь'), ('chain', 'Цепочка'), ('kill_stalker', 'Убить сталкера'), ('monster_part', 'Часть мутанта'), ('artefact', 'Принести артефакт'), ('find_item', 'Принести предмет'), ('defend_lager', 'Защитить лагерь')], max_length=255, verbose_name='Тип задания(тип цели задания)'),
        ),
        migrations.CreateModel(
            name='QuestRandomRewardThrough',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_parser.cyclicquest')),
                ('reward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_parser.questrandomreward')),
            ],
            options={
                'verbose_name': 'Рандомная награда в ЦЗ',
                'verbose_name_plural': 'Связи Цз и случайной награды',
                'unique_together': {('reward', 'quest')},
            },
        ),
        migrations.AddField(
            model_name='cyclicquest',
            name='random_rewards',
            field=models.ManyToManyField(related_name='quests', through='game_parser.QuestRandomRewardThrough', to='game_parser.questrandomreward', verbose_name='Рандомные награды'),
        ),
    ]
