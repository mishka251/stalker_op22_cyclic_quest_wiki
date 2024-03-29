# Generated by Django 4.2 on 2024-01-21 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0103_gamestoryid_spawn_section_custom'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=255)),
                ('source_file_name', models.CharField(max_length=255, verbose_name='Путь к файлу')),
                ('items_raw', models.CharField(max_length=1000, null=True, verbose_name='Строка с предметами')),
            ],
        ),
        migrations.CreateModel(
            name='ItemInTreasureBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(null=True)),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_parser.inventorybox')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_parser.baseitem')),
            ],
        ),
    ]
