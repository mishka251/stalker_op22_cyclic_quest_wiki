# Generated by Django 4.1.3 on 2023-04-03 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0069_alter_icon_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icon',
            name='icon',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='icon',
            name='name',
            field=models.CharField(max_length=512),
        ),
    ]
