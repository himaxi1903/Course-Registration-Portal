# Generated by Django 3.1.2 on 2020-10-18 22:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20201018_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.datetime(2020, 10, 18, 22, 2, 44, 228154, tzinfo=utc)),
        ),
    ]
