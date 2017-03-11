# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-11 12:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_scheduleevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='name',
            field=models.CharField(choices=[('lunch', 'Lunch'), ('dinner', 'Dinner')], default='lunch', max_length=127),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Order', verbose_name='Order'),
        ),
    ]