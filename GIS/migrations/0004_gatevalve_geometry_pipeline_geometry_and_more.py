# Generated by Django 4.0 on 2024-03-12 05:10

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GIS', '0003_alter_pipeline_condition_alter_pipeline_flow_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gatevalve',
            name='geometry',
            field=django.contrib.gis.db.models.fields.GeometryField(null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='pipeline',
            name='geometry',
            field=django.contrib.gis.db.models.fields.GeometryField(null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='storageunit',
            name='geometry',
            field=django.contrib.gis.db.models.fields.GeometryField(null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='tubewell',
            name='geometry',
            field=django.contrib.gis.db.models.fields.GeometryField(null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='storageunit',
            name='Capacity',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='storageunit',
            name='Name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='storageunit',
            name='Type',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='storageunit',
            name='Usage',
            field=models.FloatField(default=0, null=True),
        ),
    ]
