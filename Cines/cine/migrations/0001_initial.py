# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('birth_date', models.DateField(verbose_name=b'Birth_date')),
                ('image', models.ImageField(upload_to=b'image')),
            ],
            options={
                'db_table': 'actor',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'cinema',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='General',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('duration_mins', models.IntegerField()),
                ('actor', models.ManyToManyField(to='cine.Actor')),
                ('main_actor', models.ForeignKey(related_name='main_actor', to='cine.Actor')),
            ],
            options={
                'db_table': 'movie',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MovieByRoom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_datetime', models.DateTimeField(verbose_name=b'Start_datetime')),
                ('end_datetime', models.DateTimeField(verbose_name=b'')),
                ('movie', models.ForeignKey(to='cine.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('room_number', models.IntegerField()),
                ('room_manager', models.CharField(max_length=200)),
                ('cinema', models.ForeignKey(related_name='myCinema', to='cine.Cinema')),
                ('played', models.ManyToManyField(to='cine.Movie', through='cine.MovieByRoom')),
            ],
            options={
                'db_table': 'room',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='moviebyroom',
            name='room',
            field=models.ForeignKey(to='cine.Room'),
        ),
    ]
