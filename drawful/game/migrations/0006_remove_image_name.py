# Generated by Django 3.0 on 2019-12-22 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='name',
        ),
    ]
