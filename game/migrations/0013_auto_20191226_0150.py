# Generated by Django 3.0 on 2019-12-25 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_playerschoice_playersnewphrase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlinegame',
            name='playersready',
            field=models.BooleanField(default=False),
        ),
    ]
