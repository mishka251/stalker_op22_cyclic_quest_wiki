# Generated by Django 4.2 on 2024-02-15 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0125_treasure_spawn_item_alter_treasure_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='customspawnitem',
            name='custom_inventory_box',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game_parser.inventorybox', verbose_name='Тайник(рюкзак?)'),
        ),
    ]