# Generated by Django 2.1.5 on 2019-01-11 04:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistic',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.Team'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='referees',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='schedule',
            name='teams',
            field=models.ManyToManyField(through='schedule.Statistic', to='team.Team'),
        ),
        migrations.AddField(
            model_name='play',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='play',
            name='statistic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='schedule.Statistic'),
        ),
    ]