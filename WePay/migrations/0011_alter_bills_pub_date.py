# Generated by Django 4.1.3 on 2022-11-12 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("WePay", "0010_alter_bills_pub_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bills",
            name="pub_date",
            field=models.DateTimeField(default="YYYY-MM-DD HH:MM"),
        ),
    ]
