# Generated by Django 2.0 on 2018-12-20 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0061_auto_20181220_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrePayments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dueDate', models.CharField(max_length=255)),
                ('advance', models.FloatField()),
                ('lcNumberValue', models.CharField(max_length=255)),
                ('lcIssuingBank', models.CharField(max_length=255)),
                ('advanceFromBuyers', models.FloatField(blank=True, null=True)),
                ('advanceToSellers', models.FloatField(blank=True, null=True)),
                ('receivedDate', models.CharField(blank=True, max_length=255, null=True)),
                ('paidDate', models.CharField(blank=True, max_length=255, null=True)),
                ('lcExpiryDate', models.CharField(blank=True, max_length=255, null=True)),
                ('trn', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.TradeApproval')),
            ],
        ),
    ]