# Generated by Django 2.0.2 on 2018-03-14 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_participantworkshop_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParticipantStay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(default=False, help_text='Does the participant accepted the rules of the festival?', verbose_name='Are rules accepted?')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Participant', verbose_name='Participant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
