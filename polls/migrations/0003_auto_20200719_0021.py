# Generated by Django 3.0.8 on 2020-07-18 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20200718_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='percentage',
            field=models.IntegerField(default=0),
        ),
    ]
