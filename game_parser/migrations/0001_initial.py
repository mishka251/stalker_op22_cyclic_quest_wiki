# Generated by Django 4.1.3 on 2022-12-01 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_code', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CyclicQuest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('eliminate_lager', 'Уничтожить лагерь'), ('chain', 'Цепочка'), ('kill_stalker', 'Убить'), ('monster_part', 'Часть мутанта'), ('artefact', 'Принести артефакт'), ('find_item', 'Принести предмет'), ('defend_lager', 'Защитить лагерь')], max_length=255)),
                ('game_code', models.CharField(max_length=255)),
                ('giver_code', models.CharField(max_length=255, null=True)),
                ('reward_item_string', models.CharField(max_length=255, null=True)),
                ('reward_info_string', models.CharField(max_length=255, null=True)),
                ('random_rewards_string', models.CharField(max_length=255, null=True)),
                ('prior', models.IntegerField(default=0)),
                ('target_str', models.CharField(max_length=255, null=True)),
                ('giver', models.ForeignKey(max_length=255, null=True, on_delete=django.db.models.deletion.SET_NULL, to='game_parser.character')),
            ],
        ),
    ]
