# Generated by Django 2.0 on 2019-01-13 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0082_auto_20190113_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentandfinance',
            name='trn',
        ),
        migrations.DeleteModel(
            name='PaymentAndFinance',
        ),
    ]
