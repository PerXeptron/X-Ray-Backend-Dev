# Generated by Django 3.0.4 on 2020-05-29 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='XRaySample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='images/')),
                ('date_posted', models.DateTimeField(auto_now_add=True, verbose_name='date posted')),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
    ]
