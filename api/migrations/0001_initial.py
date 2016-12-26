# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-03 16:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accomodation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=127)),
                ('desc', models.TextField()),
                ('price', models.PositiveIntegerField()),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
                ('capacity', models.PositiveIntegerField(default=12)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AccomodationPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='var/photos')),
                ('desc', models.CharField(max_length=255)),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
                ('accomodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='api.Accomodation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='eg. Fish and chips', max_length=127, verbose_name='Name')),
                ('capacity', models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='Capacity')),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FoodPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='var/photos')),
                ('desc', models.CharField(max_length=255)),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='api.Food')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=127)),
                ('about', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LectorPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='var/photos')),
                ('desc', models.CharField(max_length=255)),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
                ('lector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='api.Lector')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LectorRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=127, verbose_name='Name')),
                ('slug', models.SlugField(verbose_name='Identifier')),
            ],
            options={
                'verbose_name': 'Lectors role at workshop',
                'verbose_name_plural': 'Lectors roles at workshop',
            },
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='eg. Friday lunch', max_length=127, verbose_name='Name of meal')),
                ('course', models.PositiveIntegerField(choices=[(1, 'Soup'), (2, 'Main course')], verbose_name='Course')),
                ('price', models.PositiveIntegerField(verbose_name='Price')),
                ('date', models.DateField(verbose_name='Date')),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
                ('capacity', models.PositiveIntegerField(default=12)),
            ],
            options={
                'verbose_name': 'Meal',
                'verbose_name_plural': 'Meals',
            },
        ),
        migrations.CreateModel(
            name='MealReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('food', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Food', verbose_name='Food')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Meal', verbose_name='Meal')),
            ],
            options={
                'verbose_name': 'Meal reservation',
                'verbose_name_plural': 'Meal reservations',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('symvar', models.CharField(blank=True, max_length=63)),
                ('price', models.PositiveIntegerField(verbose_name='Definitive price')),
                ('paid', models.BooleanField(default=False, verbose_name='Is paid?')),
                ('overPaid', models.BooleanField(default=False)),
                ('canceled', models.BooleanField(verbose_name='Is canceled?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('birthday', models.CharField(max_length=255)),
                ('rules', models.BooleanField(default=False)),
                ('newsletter', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('ident', models.CharField(blank=True, max_length=255, unique=True)),
                ('symvar', models.CharField(blank=True, max_length=255)),
                ('symcon', models.CharField(blank=True, max_length=255)),
                ('symspc', models.CharField(blank=True, max_length=255)),
                ('amount', models.CharField(max_length=255)),
                ('sender', models.CharField(blank=True, max_length=255)),
                ('bank', models.CharField(blank=True, max_length=255)),
                ('currency', models.CharField(blank=True, max_length=255)),
                ('received', models.DateTimeField(blank=True, null=True)),
                ('message', models.TextField(blank=True, max_length=255)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PriceLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=127, verbose_name='Name')),
                ('takes_effect_on', models.DateField(verbose_name='Date, when this price level takes effect')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('ends_at', models.DateTimeField(verbose_name='Reservation is valid until')),
                ('foods', models.ManyToManyField(through='api.MealReservation', to='api.Food', verbose_name='Foods')),
                ('meals', models.ManyToManyField(through='api.MealReservation', to='api.Meal', verbose_name='Meals')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Order', verbose_name='Order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=127, verbose_name='Team name')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Team description')),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')], default=2, verbose_name='Visibility')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=127)),
                ('desc', models.TextField()),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
                ('capacity', models.PositiveIntegerField(default=12)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkshopDifficulty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(verbose_name='Identifier')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Workshop difficulty',
                'verbose_name_plural': 'Workshop difficulties',
            },
        ),
        migrations.CreateModel(
            name='WorkshopLector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('lector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Lector', verbose_name='Lector')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.LectorRole', verbose_name='Lector role')),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Workshop', verbose_name='Workshop')),
            ],
            options={
                'verbose_name': 'Workshop lector',
                'verbose_name_plural': 'Workshop lectors',
            },
        ),
        migrations.CreateModel(
            name='WorkshopPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='var/photos')),
                ('desc', models.CharField(max_length=255)),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='api.Workshop')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkshopPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('price', models.PositiveIntegerField(verbose_name='Price in CZK')),
                ('price_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.PriceLevel', verbose_name='Price level')),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Workshop', verbose_name='Workshop')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('year', models.SlugField(unique=True, verbose_name='Year')),
                ('topic', models.TextField(blank=True, verbose_name='Topic of this year')),
                ('start_date', models.DateField(verbose_name='Date of festival start')),
                ('end_date', models.DateField(verbose_name='Date of festival end')),
                ('start_date_of_signups', models.DateField(verbose_name='Date when signups are starting')),
                ('current', models.BooleanField(verbose_name='Is this year current?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='workshop',
            name='difficulty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.WorkshopDifficulty', verbose_name='Difficulty'),
        ),
        migrations.AddField(
            model_name='workshop',
            name='lectors',
            field=models.ManyToManyField(related_name='workshops', through='api.WorkshopLector', to='api.Lector'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='workshop_price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.WorkshopPrice', verbose_name='Workshop price'),
        ),
        migrations.AddField(
            model_name='pricelevel',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Year', verbose_name='Year'),
        ),
        migrations.AddField(
            model_name='participant',
            name='assignedWorkshop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Workshop'),
        ),
        migrations.AddField(
            model_name='participant',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='order',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='api.Participant'),
        ),
        migrations.AddField(
            model_name='mealreservation',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Reservation', verbose_name='Reservation'),
        ),
        migrations.AddField(
            model_name='food',
            name='meal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Meal', verbose_name='Meal'),
        ),
    ]
