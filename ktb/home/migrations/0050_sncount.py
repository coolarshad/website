# Generated by Django 2.0 on 2018-12-19 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0049_delete_sncount'),
    ]

    operations = [
        migrations.CreateModel(
            name='SnCount',
            fields=[
                ('sn', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
    ]