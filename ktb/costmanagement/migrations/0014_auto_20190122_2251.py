# Generated by Django 2.0 on 2019-01-22 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('costmanagement', '0013_auto_20181228_1154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumptionadditive',
            name='product',
        ),
        migrations.RemoveField(
            model_name='consumptionbaseoil',
            name='product',
        ),
        migrations.DeleteModel(
            name='ConsumptionAdditive',
        ),
        migrations.DeleteModel(
            name='ConsumptionBaseOil',
        ),
    ]