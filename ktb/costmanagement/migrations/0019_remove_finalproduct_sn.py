# Generated by Django 2.0 on 2019-01-22 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('costmanagement', '0018_consumptionadditive_consumptionbaseoil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finalproduct',
            name='sn',
        ),
    ]