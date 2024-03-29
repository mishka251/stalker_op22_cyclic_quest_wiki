# Generated by Django 4.2 on 2024-02-09 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_parser', '0117_encyclopediaarticle_artefact_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anomaly_id', models.CharField(max_length=255)),
                ('anomaly_name', models.CharField(max_length=255)),
                ('condition_raw', models.CharField(max_length=255)),
                ('components_raw', models.CharField(max_length=255)),
                ('cel_raw', models.CharField(max_length=255)),
                ('v_udachi', models.DecimalField(decimal_places=3, max_digits=6)),
                ('v_virogd', models.DecimalField(decimal_places=3, max_digits=6)),
                ('v_ottorg', models.DecimalField(decimal_places=3, max_digits=6)),
                ('vremya_day', models.CharField(max_length=255)),
                ('vremya_hour', models.CharField(max_length=255)),
                ('vremya_min', models.CharField(max_length=255)),
                ('remove_anomaly', models.BooleanField()),
                ('not_for_mutator', models.BooleanField()),
                ('info_raw', models.CharField(max_length=255)),
                ('cel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cooking_in_recepts', to='game_parser.baseitem')),
                ('components', models.ManyToManyField(related_name='use_in_recepts', to='game_parser.baseitem')),
                ('condition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='opening_recepts', to='game_parser.infoportion')),
                ('info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='get_from_recept', to='game_parser.infoportion')),
            ],
        ),
    ]
