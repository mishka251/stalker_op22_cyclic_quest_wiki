# Generated by Django 4.2 on 2024-01-12 21:10

from django.db import migrations, models


def move_trader_data(apps, schema_editor):
    Trader = apps.get_model("game_parser", "Trader")
    Trader2 = apps.get_model("game_parser", "Trader2")
    db_alias = schema_editor.connection.alias
    new_traders = [
        Trader2(
            id=old_trader.id,
            game_code=old_trader.game_code,
            name=old_trader.name,
        )
        for old_trader in Trader.objects.using(db_alias).all()
    ]
    Trader2.objects.using(db_alias).bulk_create(
        new_traders
    )


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0090_alter_spawnitem_game_vertex_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trader2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_code', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255, null=True)),
                ('source_file', models.CharField(max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Профиль торговли',
                'verbose_name_plural': 'Профили торговли',
            },
        ),
        migrations.AlterModelOptions(
            name='spawnitem',
            options={'verbose_name': 'Секция спавна', 'verbose_name_plural': 'Секции спавна'},
        ),
        migrations.RunPython(move_trader_data),
    ]