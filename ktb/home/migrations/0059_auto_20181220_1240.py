# Generated by Django 2.0 on 2018-12-20 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0058_auto_20181220_1040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prepayments',
            name='trn',
        ),
        migrations.DeleteModel(
            name='PrePayments',
        ),
    ]
