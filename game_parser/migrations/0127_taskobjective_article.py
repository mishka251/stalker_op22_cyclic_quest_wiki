# Generated by Django 4.2 on 2024-02-18 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0126_customspawnitem_custom_inventory_box'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskobjective',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_objectives', to='game_parser.encyclopediaarticle', verbose_name='Статья'),
        ),
    ]
