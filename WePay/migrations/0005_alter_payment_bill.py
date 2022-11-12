# Generated by Django 4.1.3 on 2022-11-12 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("WePay", "0004_bills_is_closed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="bill",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payments",
                to="WePay.bills",
            ),
        ),
    ]
