# Generated by Django 4.2 on 2024-03-06 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0131_alter_storylinecharacter_game_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorybox',
            name='visual_str',
            field=models.CharField(max_length=255, null=True, verbose_name='Внешний вид(название - visual)'),
        ),
        migrations.AlterField(
            model_name='inventorybox',
            name='source_file_name',
            field=models.CharField(max_length=255, verbose_name='Путь к файлу(custom_data)'),
        ),
    ]