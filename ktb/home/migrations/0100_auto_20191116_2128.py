# Generated by Django 2.2.7 on 2019-11-16 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0099_auto_20190905_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradeapproval',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='tradeapproval',
            name='remarks',
            field=models.TextField(),
        ),
    ]
