# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-13 18:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20170312_2348'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('capacity', models.PositiveIntegerField(blank=True, help_text='How many people can fit in', null=True, verbose_name='Capacity')),
                ('name', models.CharField(help_text='eg. Fish and chips', max_length=127, verbose_name='Name')),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='food',
            name='capacity',
        ),
        migrations.RemoveField(
            model_name='food',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='food',
            name='id',
        ),
        migrations.RemoveField(
            model_name='food',
            name='meal',
        ),
        migrations.RemoveField(
            model_name='food',
            name='name',
        ),
        migrations.RemoveField(
            model_name='food',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='food',
            name='visibility',
        ),
        migrations.RemoveField(
            model_name='meal',
            name='course',
        ),
        migrations.AlterField(
            model_name='foodphoto',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='api.AbstractFood'),
        ),
        migrations.CreateModel(
            name='Soup',
            fields=[
                ('abstractfood_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.AbstractFood')),
            ],
            options={
                'abstract': False,
            },
            bases=('api.abstractfood',),
        ),
        migrations.AddField(
            model_name='abstractfood',
            name='meal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Meal', verbose_name='Meal'),
        ),
        migrations.AddField(
            model_name='food',
            name='abstractfood_ptr',
            field=models.OneToOneField(auto_created=True, default=None, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.AbstractFood'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mealreservation',
            name='soup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Soup', verbose_name='Soup'),
        ),
    ]
