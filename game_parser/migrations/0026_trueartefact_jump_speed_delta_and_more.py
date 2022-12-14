# Generated by Django 4.1.3 on 2022-12-13 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0025_trueartefact_additional_weight_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trueartefact',
            name='jump_speed_delta',
            field=models.DecimalField(decimal_places=3, max_digits=5, null=True, verbose_name='Прыжок'),
        ),
        migrations.AddField(
            model_name='trueartefact',
            name='psy_health_restore_speed',
            field=models.DecimalField(decimal_places=5, max_digits=7, null=True, verbose_name='Пси-здоровье?'),
        ),
        migrations.AddField(
            model_name='trueartefact',
            name='satiety_restore_speed',
            field=models.DecimalField(decimal_places=5, max_digits=7, null=True, verbose_name='???'),
        ),
    ]
