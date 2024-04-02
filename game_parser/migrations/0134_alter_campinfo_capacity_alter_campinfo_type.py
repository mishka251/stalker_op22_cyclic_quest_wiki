# Generated by Django 4.2 on 2024-04-01 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0133_campinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campinfo',
            name='capacity',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='campinfo',
            name='type',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
