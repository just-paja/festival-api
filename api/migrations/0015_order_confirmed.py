# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-15 00:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20170314_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='confirmed',
            field=models.BooleanField(default=False, verbose_name='Is confirmed?'),
        ),
    ]
