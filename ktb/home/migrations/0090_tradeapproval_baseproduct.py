# Generated by Django 2.0 on 2019-04-01 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0089_auto_20190210_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradeapproval',
            name='baseproduct',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]