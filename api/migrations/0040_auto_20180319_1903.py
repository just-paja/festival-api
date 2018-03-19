# Generated by Django 2.0.1 on 2018-03-19 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_participantstay_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='bank',
            field=models.CharField(blank=True, default='unknown', help_text='Bank sending this payment', max_length=255, null=True, verbose_name='Bank'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(blank=True, default='unknown', help_text='Currency of the payment', max_length=255, null=True, verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='sender',
            field=models.CharField(blank=True, default='unknown', help_text='Account number of person sending this payment', max_length=255, null=True, verbose_name='Sender'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user_identification',
            field=models.CharField(blank=True, help_text='User identification given by the bank', max_length=255, null=True, verbose_name='User identification'),
        ),
    ]
