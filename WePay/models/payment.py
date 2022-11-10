# from django.contrib import admin
from abc import abstractmethod
from typing import Any

import omise
from django.db import models
from django.utils import timezone

from .bill import Bills
from .userprofile import UserProfile

OMISE_PUBLIC = "pkey_test_5tgganhu45npoycv190"
OMISE_SECRET = "skey_test_5tecjczxmlxrbtfxhw9"

omise.api_public = OMISE_PUBLIC
omise.api_secret = OMISE_SECRET


class Payment(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True
    )
    date = models.DateTimeField(null=True, blank=True)
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE)
    uri = models.CharField(max_length=100, null=True, blank=True)

    class Status_choice(models.TextChoices):
        """choice for status whether PAID, PENDING, or UNPAID"""

        PAID = "PAID"
        PENDING = "PENDING"
        UNPAID = "UNPAID"

    status = models.CharField(
        choices=Status_choice.choices, default=Status_choice.UNPAID, max_length=10
    )

    class PaymentChoice(models.TextChoices):
        """choice for payment"""

        CASH = "Cash"
        PROMPTPAY = "PromptPay"
        SCB = "SCB"
        KTB = "KTB"
        BAY = "BAY"
        BBL = "BBL"

    payment_type = models.CharField(
        choices=PaymentChoice.choices, default=PaymentChoice.CASH, max_length=10
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """set header status to paid"""
        super().__init__(*args, **kwargs)
        if self.user == self.bill.header:
            self.user.status = self.Status_choice.PAID
            self.user.save()
        self.payment_dct = {
            "Cash": CashPayment,
            "PromptPay": PromptPayPayment,
            "SCB": SCBPayment,
            "KTB": KTBPayment,
            "BAY": BAYPayment,
            "BBL": BBLPayment,
        }

    @property
    def header(self) -> UserProfile:
        """Get header of each bill in each payment"""
        return self.bill.header

    @property
    def amount(self) -> int:
        """get amount of each payment"""
        if self.payment_type == self.PaymentChoice.CASH:
            return int(self.bill.calculate_price(self.user))
        return int(self.bill.calculate_price(self.user) * 100)

    @property
    def selected_payment(self) -> Any:
        """get now payment"""
        return self.payment_dct[self.payment_type]

    def pay(self) -> None:
        """Pay to header"""
        if self.status in (self.Status_choice.PAID):
            return
        now_payment = self.selected_payment.objects.get_or_create(payment=self)[0]
        now_payment.pay()
        self.save()

    def __repr__(self) -> str:
        """represent a payment"""
        return f"Payment(user={self.user}, date={self.date}, bill={self.bill}, status={self.status}, payment_type={self.payment_type})"

    __str__ = __repr__


class BasePayment(models.Model):
    """Entry model"""

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default=None)

    @abstractmethod
    def pay(self):
        pass

    class Meta:
        abstract = True

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.__str__ = cls.__repr__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.payment.payment_type}, {self.payment.status}, {self.payment.user})"


class OmisePayment(BasePayment):
    charge_id = models.CharField(max_length=100, null=True, blank=True)
    payment_type = models.CharField(max_length=100, default="promptpay")
    # i dont know how to call this on Payment class, So I will move up it up to payment class
    # uri = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True

    def pay(self):
        """pay by omise"""
        # amount must morethan 20
        if self.payment.status == self.payment.Status_choice.UNPAID:
            source = omise.Source.create(
                type=self.payment_type,
                amount=self.payment.amount,
                currency="thb",
            )

            omise.api_secret = self.payment.bill.header.chain.key

            charge = omise.Charge.create(
                amount=self.payment.amount,
                currency="thb",
                source=source.id,
                return_uri=f"http://127.0.0.1:8000/payment/{self.payment.id}/update",
            )

            self.charge_id = charge.id
            self.payment.uri = charge.authorize_uri
        self.update_status()
        print(omise.api_secret)

    def update_status(self):  # TODO: Move this mothod to Payment class
        print(omise.api_secret)
        status = omise.Charge.retrieve(self.charge_id).status
        print(status)
        if status == "successful":
            self.payment.status = self.payment.Status_choice.PAID
        elif status == "pending":
            self.payment.status = self.payment.Status_choice.PENDING
        else:
            self.payment.status = self.payment.Status_choice.UNPAID
        self.payment.save()
        print(self.payment.status)
        self.save()


class PromptPayPayment(OmisePayment):
    payment_type = "promptpay"


class SCBPayment(OmisePayment):
    payment_type = "internet_banking_scb"


class KTBPayment(OmisePayment):
    payment_type = "internet_banking_ktb"


class BBLPayment(OmisePayment):
    payment_type = "internet_banking_bbl"


class BAYPayment(OmisePayment):
    payment_type = "internet_banking_bay"


class CashPayment(BasePayment):
    def pay(self):
        if self.payment.status == self.payment.Status_choice.PAID:
            return

        self.payment.status = self.payment.Status_choice.PAID
        self.payment.save()
