# Generated by Django 2.0 on 2018-11-28 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_salesandpurchase'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovdBy',
            fields=[
                ('trn', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='home.TradeApproval')),
                ('manager1', models.CharField(max_length=255)),
                ('manager2', models.CharField(max_length=255)),
                ('approve1', models.BooleanField()),
                ('approve2', models.BooleanField()),
            ],
        ),
    ]
