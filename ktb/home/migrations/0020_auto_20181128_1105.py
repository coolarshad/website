# Generated by Django 2.0 on 2018-11-28 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_salesandpurchase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesandpurchase',
            name='trn',
        ),
        migrations.DeleteModel(
            name='SalesAndPurchase',
        ),
    ]