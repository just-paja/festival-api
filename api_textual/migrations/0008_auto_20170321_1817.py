# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-21 18:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_textual', '0007_auto_20170321_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollanswer',
            name='performer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polls', to='api_textual.Performer'),
        ),
    ]
