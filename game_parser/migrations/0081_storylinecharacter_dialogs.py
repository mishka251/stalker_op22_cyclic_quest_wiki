# Generated by Django 4.2 on 2023-04-17 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0080_remove_cyclicquest_giver_cyclicquest_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='storylinecharacter',
            name='dialogs',
            field=models.ManyToManyField(to='game_parser.dialog'),
        ),
    ]
