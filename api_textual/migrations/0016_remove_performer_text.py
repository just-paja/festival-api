# Generated by Django 2.0.1 on 2018-03-06 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_textual', '0015_performer_texts_20180306_0857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performer',
            name='text',
        ),
    ]
