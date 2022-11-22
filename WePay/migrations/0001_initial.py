# Generated by Django 4.1 on 2022-11-20 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Bills",
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
                ("name", models.CharField(max_length=100, null=True)),
                ("pub_date", models.DateTimeField(default="2022-11-20 21:42:31")),
                ("is_created", models.BooleanField(default=False)),
                ("is_closed", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Bill",
                "verbose_name_plural": "Bills",
            },
        ),
        migrations.CreateModel(
            name="Payment",
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
                        blank=True, default="2022-11-20 21:42:31", null=True
                    ),
                ),
                ("uri", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PAID", "Paid"),
                            ("PENDING", "Pending"),
                            ("UNPAID", "Unpaid"),
                            ("FAIL", "Fail"),
                            ("EXPIRED", "Expired"),
                        ],
                        default="UNPAID",
                        max_length=10,
                    ),
                ),
                (
                    "payment_type",
                    models.CharField(
                        choices=[
                            ("Cash", "Cash"),
                            ("PromptPay", "Promptpay"),
                            ("SCB", "Scb"),
                            ("KTB", "Ktb"),
                            ("BAY", "Bay"),
                            ("BBL", "Bbl"),
                        ],
                        default="Cash",
                        max_length=10,
                    ),
                ),
                (
                    "bill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="WePay.bills",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
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
                ("chain_id", models.CharField(default="", max_length=100)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Topic",
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
                ("title", models.CharField(max_length=100)),
                ("price", models.PositiveIntegerField()),
                (
                    "bill",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="WePay.bills",
                    ),
                ),
                (
                    "user",
                    models.ManyToManyField(
                        related_name="topic", to="WePay.userprofile"
                    ),
                ),
            ],
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
                ("charge_id", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "payment",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to="WePay.payment",
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
                ("charge_id", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "payment",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to="WePay.payment",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="payment",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="WePay.userprofile",
            ),
        ),
        migrations.CreateModel(
            name="KTBPayment",
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
                ("charge_id", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "payment",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to="WePay.payment",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CashPayment",
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
                    "payment",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to="WePay.payment",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="bills",
            name="header",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="WePay.userprofile"
            ),
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
                ("charge_id", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "payment",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to="WePay.payment",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
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
                ("charge_id", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "payment",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to="WePay.payment",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
