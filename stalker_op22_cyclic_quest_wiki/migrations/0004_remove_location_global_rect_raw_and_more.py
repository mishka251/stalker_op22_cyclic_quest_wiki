# Generated by Django 4.2.11 on 2024-04-11 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stalker_op22_cyclic_quest_wiki', '0003_alter_translation_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='global_rect_raw',
        ),
        migrations.RemoveField(
            model_name='location',
            name='offset_str',
        ),
        migrations.RemoveField(
            model_name='locationmapinfo',
            name='bound_rect_raw',
        ),
    ]