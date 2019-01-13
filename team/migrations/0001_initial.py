# Generated by Django 2.1.5 on 2019-01-12 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=4)),
                ('caption', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lead_team', related_query_name='lead_team', to='player.Student')),
                ('managers', models.ManyToManyField(related_name='manage_team', related_query_name='vice_leading_team', to='player.Student')),
                ('players', models.ManyToManyField(to='player.Student')),
                ('vice_caption', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vice_lead_team', related_query_name='vice_lead_team', to='player.Student')),
            ],
        ),
    ]
