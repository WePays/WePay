# Generated by Django 4.1 on 2022-10-30 12:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("WePay", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cashpayment",
            name="bill",
            field=models.ForeignKey(
                default=datetime.datetime(
                    2022, 10, 30, 12, 58, 22, 772239, tzinfo=datetime.timezone.utc
                ),
                on_delete=django.db.models.deletion.CASCADE,
                to="WePay.bills",
            ),
        ),
        migrations.AlterField(
            model_name="omisepayment",
            name="bill",
            field=models.ForeignKey(
                default=datetime.datetime(
                    2022, 10, 30, 12, 58, 22, 772239, tzinfo=datetime.timezone.utc
                ),
                on_delete=django.db.models.deletion.CASCADE,
                to="WePay.bills",
            ),
        ),
    ]