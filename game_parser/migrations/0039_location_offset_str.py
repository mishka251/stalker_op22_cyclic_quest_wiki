# Generated by Django 4.1.3 on 2023-01-02 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game_parser", "0038_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="location",
            name="offset_str",
            field=models.CharField(max_length=255, null=True, verbose_name="Сдвиг на глобальной карте??"),
        ),
    ]
