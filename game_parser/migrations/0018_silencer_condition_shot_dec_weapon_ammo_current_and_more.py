# Generated by Django 4.1.3 on 2022-12-11 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0017_ammo_buck_shot_ammo_explosive_str_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='silencer',
            name='condition_shot_dec',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=12, verbose_name='знос за 1 выстрел'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weapon',
            name='ammo_current',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='weapon',
            name='slot',
            field=models.IntegerField(null=True),
        ),
    ]
