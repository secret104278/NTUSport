# Generated by Django 2.1.5 on 2019-01-11 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='grade',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
