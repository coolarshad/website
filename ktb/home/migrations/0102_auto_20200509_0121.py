# Generated by Django 2.1.4 on 2020-05-08 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0101_auto_20191116_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesandpurchase',
            name='batch_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='salesandpurchase',
            name='production_date',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]