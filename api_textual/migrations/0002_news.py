# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-30 16:55
from __future__ import unicode_literals

from django.db import migrations, models
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        ('api_textual', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=127, verbose_name='Name')),
                ('slug', models.SlugField(verbose_name='Identifier in URL')),
                ('text', django_markdown.models.MarkdownField(verbose_name='Text')),
            ],
            options={
                'verbose_name_plural': 'News list',
                'verbose_name': 'News',
            },
        ),
    ]
