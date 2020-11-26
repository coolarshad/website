# Generated by Django 2.0 on 2018-12-19 04:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0044_auto_20181218_2313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approvedby',
            name='trn',
        ),
        migrations.RemoveField(
            model_name='disputes',
            name='trn',
        ),
        migrations.RemoveField(
            model_name='extracost',
            name='trn',
        ),
        migrations.DeleteModel(
            name='InventorySn',
        ),
        migrations.DeleteModel(
            name='Kyc',
        ),
        migrations.RemoveField(
            model_name='paymentandfinance',
            name='trn',
        ),
        migrations.RemoveField(
            model_name='pl',
            name='trn',
        ),
        migrations.RemoveField(
            model_name='prepayments',
            name='trn',
        ),
        migrations.DeleteModel(
            name='Products',
        ),
        migrations.RemoveField(
            model_name='salesandpurchase',
            name='trn',
        ),
        migrations.DeleteModel(
            name='SaveInventory',
        ),
        migrations.DeleteModel(
            name='SnCount',
        ),
        migrations.DeleteModel(
            name='SnStock',
        ),
        migrations.DeleteModel(
            name='StockJournal',
        ),
        migrations.DeleteModel(
            name='StockNo',
        ),
        migrations.DeleteModel(
            name='TradeRefNo',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.DeleteModel(
            name='ApprovedBy',
        ),
        migrations.DeleteModel(
            name='Disputes',
        ),
        migrations.DeleteModel(
            name='ExtraCost',
        ),
        migrations.DeleteModel(
            name='PaymentAndFinance',
        ),
        migrations.DeleteModel(
            name='PL',
        ),
        migrations.DeleteModel(
            name='PrePayments',
        ),
        migrations.DeleteModel(
            name='SalesAndPurchase',
        ),
        migrations.DeleteModel(
            name='TradeApproval',
        ),
    ]