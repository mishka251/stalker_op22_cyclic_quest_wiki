# Generated by Django 4.2 on 2024-01-02 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0085_questrandomreward_icon_questrandomreward_index_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='weapon',
            name='ammo',
            field=models.ManyToManyField(to='game_parser.ammo', verbose_name='Патроны'),
        ),
        migrations.AddField(
            model_name='weapon',
            name='grenade_launcher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game_parser.grenadelauncher', verbose_name='Подствольник'),
        ),
        migrations.AddField(
            model_name='weapon',
            name='scope',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game_parser.scope', verbose_name='Прицел'),
        ),
        migrations.AddField(
            model_name='weapon',
            name='silencer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game_parser.silencer', verbose_name='Глушитель'),
        ),
    ]
