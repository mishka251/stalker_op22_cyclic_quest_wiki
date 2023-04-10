# Generated by Django 4.1.3 on 2023-03-23 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0043_remove_treasure_name_translation'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseScriptReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='Название')),
                ('namespace', models.CharField(max_length=512, verbose_name='Название файла')),
            ],
            options={
                'verbose_name': 'Диалог',
            },
        ),
        migrations.CreateModel(
            name='MoneyReward',
            fields=[
                ('basescriptreward_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='game_parser.basescriptreward')),
                ('count', models.DecimalField(decimal_places=2, max_digits=20)),
                ('raw_count', models.CharField(max_length=512)),
            ],
            bases=('game_parser.basescriptreward',),
        ),
        migrations.CreateModel(
            name='ScriptFunction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='Название')),
                ('namespace', models.CharField(max_length=512, verbose_name='Название файла')),
                ('dialog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actions', to='game_parser.dialog')),
            ],
            options={
                'verbose_name': 'Функция из скриптов',
            },
        ),
        migrations.AddField(
            model_name='basescriptreward',
            name='function',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rewards', to='game_parser.scriptfunction'),
        ),
        migrations.CreateModel(
            name='SpawnReward',
            fields=[
                ('basescriptreward_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='game_parser.basescriptreward')),
                ('raw_maybe_item', models.CharField(max_length=512)),
                ('raw_call', models.CharField(max_length=512)),
                ('x', models.FloatField(null=True)),
                ('y', models.FloatField(null=True)),
                ('z', models.FloatField(null=True)),
                ('level_vertex', models.IntegerField(null=True)),
                ('game_vertex_id', models.IntegerField(null=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game_parser.baseitem', verbose_name='Предмет')),
            ],
            bases=('game_parser.basescriptreward',),
        ),
        migrations.CreateModel(
            name='ItemReward',
            fields=[
                ('basescriptreward_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='game_parser.basescriptreward')),
                ('raw_item', models.CharField(max_length=512)),
                ('count', models.IntegerField()),
                ('raw_count', models.CharField(max_length=512)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game_parser.baseitem', verbose_name='Предмет')),
            ],
            bases=('game_parser.basescriptreward',),
        ),
    ]