# Generated by Django 3.0 on 2019-12-16 20:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Phrase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('gamesCount', models.IntegerField(default=0)),
                ('rating', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='PhrasePack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('rating', models.FloatField(default=0.0)),
                ('gamesCount', models.IntegerField(default=0)),
                ('phrases', models.ManyToManyField(to='game.Phrase')),
            ],
        ),
        migrations.CreateModel(
            name='PlayedGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playDate', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('phrasePack', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.PhrasePack')),
                ('players', models.ManyToManyField(to='user_profile.Profile')),
            ],
        ),
    ]
