# Generated by Django 2.0 on 2019-07-07 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costmanagement', '0030_auto_20190524_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumption',
            name='date',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='consumption',
            name='sn',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='finalproduct',
            name='date',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='finalproduct',
            name='sn',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
