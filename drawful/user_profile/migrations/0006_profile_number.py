# Generated by Django 3.0 on 2019-12-23 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0005_auto_20191222_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='number',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
