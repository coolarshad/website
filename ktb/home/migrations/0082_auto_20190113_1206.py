# Generated by Django 2.0 on 2019-01-13 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0081_purchaseproducttrace_salesproducttrace'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentandfinance',
            name='logisticsCommisionDueDate',
        ),
        migrations.AddField(
            model_name='paymentandfinance',
            name='agentCommissionDueDate',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='paymentandfinance',
            name='logisticsCommissionDueDate',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
