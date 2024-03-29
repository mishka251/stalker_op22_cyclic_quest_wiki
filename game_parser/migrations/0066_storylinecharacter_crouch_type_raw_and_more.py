# Generated by Django 4.1.3 on 2023-04-02 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0065_storylinecharacter_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='storylinecharacter',
            name='crouch_type_raw',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='storylinecharacter',
            name='money_inf_raw',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='storylinecharacter',
            name='money_max_raw',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='storylinecharacter',
            name='money_min_raw',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='storylinecharacter',
            name='snd_config_raw',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
