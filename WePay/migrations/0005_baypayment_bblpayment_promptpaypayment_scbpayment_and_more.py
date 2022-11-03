# Generated by Django 4.1 on 2022-11-02 08:42

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("WePay", "0004_alter_cashpayment_date_alter_omisepayment_date_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BAYPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2022, 11, 2, 8, 42, 16, 318839, tzinfo=datetime.timezone.utc
                        )
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PAID", "Paid"),
                            ("PENDING", "Pending"),
                            ("UNPAID", "Unpaid"),
                        ],
                        default="UNPAID",
                        max_length=10,
                    ),
                ),
                ("charge_id", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "bill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="WePay.bills"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="WePay.userprofile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="BBLPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2022, 11, 2, 8, 42, 16, 318839, tzinfo=datetime.timezone.utc
                        )
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PAID", "Paid"),
                            ("PENDING", "Pending"),
                            ("UNPAID", "Unpaid"),
                        ],
                        default="UNPAID",
                        max_length=10,
                    ),
                ),
                ("charge_id", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "bill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="WePay.bills"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="WePay.userprofile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PromptPayPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2022, 11, 2, 8, 42, 16, 318839, tzinfo=datetime.timezone.utc
                        )
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PAID", "Paid"),
                            ("PENDING", "Pending"),
                            ("UNPAID", "Unpaid"),
                        ],
                        default="UNPAID",
                        max_length=10,
                    ),
                ),
                ("charge_id", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "bill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="WePay.bills"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="WePay.userprofile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SCBPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2022, 11, 2, 8, 42, 16, 318839, tzinfo=datetime.timezone.utc
                        )
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PAID", "Paid"),
                            ("PENDING", "Pending"),
                            ("UNPAID", "Unpaid"),
                        ],
                        default="UNPAID",
                        max_length=10,
                    ),
                ),
                ("charge_id", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "bill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="WePay.bills"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="WePay.userprofile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="STBPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2022, 11, 2, 8, 42, 16, 318839, tzinfo=datetime.timezone.utc
                        )
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PAID", "Paid"),
                            ("PENDING", "Pending"),
                            ("UNPAID", "Unpaid"),
                        ],
                        default="UNPAID",
                        max_length=10,
                    ),
                ),
                ("charge_id", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "bill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="WePay.bills"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="WePay.userprofile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AlterField(
            model_name="cashpayment",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2022, 11, 2, 8, 42, 16, 318839, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.DeleteModel(
            name="OmisePayment",
        ),
    ]