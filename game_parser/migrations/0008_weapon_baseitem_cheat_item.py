# Generated by Django 4.1.3 on 2022-12-05 21:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0007_baseitem_ammo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('baseitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='game_parser.baseitem')),
                ('ef_main_weapon_type', models.CharField(max_length=10)),
                ('ef_weapon_type', models.CharField(max_length=10)),
                ('weapon_class', models.CharField(max_length=255)),
                ('ammo_mag_size', models.PositiveIntegerField(verbose_name='Размер магазина')),
                ('fire_modes_str', models.CharField(max_length=255, verbose_name='Режимы стрельбы(сырая строка)')),
                ('ammo_class_str', models.CharField(max_length=1000, verbose_name='Боеприпасы')),
                ('grenade_class_str', models.CharField(max_length=1000, verbose_name='Типы гранат для подствольника')),
                ('rpm', models.IntegerField(verbose_name='Скорострельность выстрелов в минуту')),
                ('scope_status_str', models.CharField(max_length=5, verbose_name='Возможность установки прицела')),
                ('silencer_status_str', models.CharField(max_length=5, verbose_name='Возможность установки глушителя')),
                ('grenade_launcher_status', models.CharField(max_length=5, verbose_name='Возможность установки ГП')),
                ('scope_name', models.CharField(max_length=255, verbose_name='Название прицела')),
                ('silencer_name', models.CharField(max_length=255, verbose_name='Название глушителя')),
                ('grenade_launcher_name', models.CharField(max_length=255, verbose_name='Название ГП')),
            ],
            bases=('game_parser.baseitem',),
        ),
        migrations.AddField(
            model_name='baseitem',
            name='cheat_item',
            field=models.BooleanField(default=False),
        ),
    ]
