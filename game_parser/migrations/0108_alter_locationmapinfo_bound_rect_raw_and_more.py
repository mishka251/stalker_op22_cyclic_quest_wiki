# Generated by Django 4.2 on 2024-01-25 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0107_alter_locationmapinfo_texture_raw'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationmapinfo',
            name='bound_rect_raw',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='locationmapinfo',
            name='global_rect_raw',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
