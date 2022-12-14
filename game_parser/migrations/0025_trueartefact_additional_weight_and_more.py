# Generated by Django 4.1.3 on 2022-12-13 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0024_alter_trueartefact_burn_immunity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trueartefact',
            name='additional_weight',
            field=models.DecimalField(decimal_places=3, max_digits=5, null=True, verbose_name='Переносимый вес'),
        ),
        migrations.AddField(
            model_name='trueartefact',
            name='bleeding_restore_speed',
            field=models.DecimalField(decimal_places=3, max_digits=5, null=True, verbose_name='Кровотечение?'),
        ),
        migrations.AddField(
            model_name='trueartefact',
            name='power_restore_speed',
            field=models.DecimalField(decimal_places=3, max_digits=5, null=True, verbose_name='Восстановление сил'),
        ),
        migrations.AddField(
            model_name='trueartefact',
            name='radiation_restore_speed',
            field=models.DecimalField(decimal_places=3, max_digits=5, null=True, verbose_name='Радиация?'),
        ),
    ]
