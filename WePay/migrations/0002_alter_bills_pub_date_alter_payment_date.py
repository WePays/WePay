# Generated by Django 4.1.3 on 2022-11-30 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("WePay", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bills",
            name="pub_date",
            field=models.DateTimeField(default="2022-11-30 09:32:16"),
        ),
        migrations.AlterField(
            model_name="payment",
            name="date",
            field=models.DateTimeField(
                blank=True, default="2022-11-30 09:32:16", null=True
            ),
        ),
    ]
