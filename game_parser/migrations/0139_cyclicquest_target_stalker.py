# Generated by Django 4.2 on 2024-04-03 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0138_remove_cyclicquest_target_stalker'),
    ]

    operations = [
        migrations.AddField(
            model_name='cyclicquest',
            name='target_stalker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game_parser.stalkersection', verbose_name='Сталкер цель'),
        ),
    ]
