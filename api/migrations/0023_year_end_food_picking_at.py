# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-17 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_participanttoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='year',
            name='end_food_picking_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Last day participants can pick food'),
        ),
    ]
