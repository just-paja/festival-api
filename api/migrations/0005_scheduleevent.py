# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-23 19:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_textual', '0005_performer_performerphoto'),
        ('api', '0004_auto_20170213_0116'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=127, verbose_name='Name')),
                ('start_at', models.DateTimeField(verbose_name='Event start time')),
                ('end_at', models.DateTimeField(blank=True, null=True, verbose_name='Event end time')),
                ('performer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='api_textual.Performer')),
                ('workshops', models.ManyToManyField(blank=True, to='api.Workshop')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='api.Year', verbose_name='Year')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]