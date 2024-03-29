# Generated by Django 4.2 on 2024-02-15 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0124_alter_taskobjective_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='treasure',
            name='spawn_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game_parser.spawnitem', verbose_name='Секция спавна'),
        ),
        migrations.AlterField(
            model_name='treasure',
            name='target',
            field=models.CharField(max_length=10, verbose_name='spawn_id для поиска в спавне'),
        ),
    ]
