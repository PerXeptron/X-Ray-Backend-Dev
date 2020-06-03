# Generated by Django 3.0.4 on 2020-06-02 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samplexray', '0005_remove_xraysample_diseaselist_dict'),
    ]

    operations = [
        migrations.AddField(
            model_name='xraysample',
            name='cool',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='xraysample',
            name='fist',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='xraysample',
            name='ok',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='xraysample',
            name='stop',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='xraysample',
            name='yo',
            field=models.FloatField(default=0.0),
        ),
    ]
