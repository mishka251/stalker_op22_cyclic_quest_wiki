# Generated by Django 4.1.3 on 2022-12-25 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0030_translation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='translation',
            name='fra',
            field=models.TextField(default='', verbose_name='Французский'),
            preserve_default=False,
        ),
    ]
