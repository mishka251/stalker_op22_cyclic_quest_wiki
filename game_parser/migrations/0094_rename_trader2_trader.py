# Generated by Django 4.2 on 2024-01-12 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0093_delete_trader'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Trader2',
            new_name='Trader',
        ),
    ]