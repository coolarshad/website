# Generated by Django 2.0 on 2018-12-30 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0070_pl'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logdate', models.DateField()),
                ('user', models.CharField(max_length=255)),
                ('authority', models.CharField(max_length=255)),
                ('action', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('-logdate',),
            },
        ),
    ]