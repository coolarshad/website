# Generated by Django 2.0 on 2018-12-18 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0042_auto_20181218_2242'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeApproval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.IntegerField()),
                ('company', models.CharField(max_length=255)),
                ('trd', models.DateField(blank=True, null=True)),
                ('trn', models.CharField(max_length=255)),
                ('types', models.CharField(max_length=255)),
                ('product', models.CharField(max_length=255)),
                ('origin', models.CharField(max_length=255)),
                ('client', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('tad', models.DateField(blank=True, null=True)),
                ('trade_status', models.CharField(max_length=255)),
                ('tcq', models.CharField(max_length=255)),
                ('tolerance', models.CharField(max_length=255)),
                ('packing', models.CharField(max_length=255)),
                ('tuq', models.CharField(max_length=255)),
                ('ratePMT', models.FloatField()),
                ('commissionAgent', models.CharField(max_length=255)),
                ('commissionRate', models.FloatField()),
                ('logisticProvider', models.CharField(max_length=255)),
                ('estimatedLogisticsCost', models.FloatField()),
                ('paymentTerm', models.CharField(max_length=255)),
                ('incoterm', models.CharField(max_length=255)),
                ('pod', models.CharField(max_length=255)),
                ('etd', models.DateField(blank=True, null=True)),
                ('eta', models.DateField(blank=True, null=True)),
                ('po_number', models.CharField(max_length=255)),
                ('po_date', models.DateField(blank=True, null=True)),
                ('so_number', models.CharField(max_length=255)),
                ('so_date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]