# from django.contrib import admin
from abc import abstractmethod
from typing import Any
from django.db import models
from django.utils import timezone
from .userprofile import UserProfile
from .bill import Bills

import omise

OMISE_PUBLIC = 'pkey_test_5tgganhu45npoycv190'
OMISE_SECRET = 'skey_test_5tecjczxmlxrbtfxhw9'

omise.api_public = OMISE_PUBLIC
omise.api_secret = OMISE_SECRET


class BasePayment(models.Model):
    """Entry model"""

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.localtime)
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE)

    @abstractmethod
    def pay(self):
        pass

    class Status_choice(models.TextChoices):
        PAID = "PAID"
        PENDING = 'PENDING'
        UNPAID = "UNPAID"

    status = models.CharField(
        choices=Status_choice.choices, default=Status_choice.UNPAID, max_length=10
    )

    class Meta:
        abstract = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.user == self.bill.header:
            self.user.status = self.Status_choice.PAID

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.__str__ = cls.__repr__

    def get_status(self):
        return self.status

    @property
    def header(self):
        return self.bill.header

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(user={self.user}, date={self.date},\
    bill={self.bill}, status={self.status})"


class OmisePayment(BasePayment):
    charge_id = models.CharField(max_length=100, null=True, blank=True)

    class PaymentChoice(models.TextChoices):
        PROMPT_PAY = "promptpay"
        SCB = "internet_banking_scb"
        STB = "internet_banking_ktb"
        BBL = "internet_banking_bbl"
        BAY = "internet_banking_bay"

    payment_type = models.CharField(
        choices=PaymentChoice.choices, max_length=20, default=PaymentChoice.PROMPT_PAY
    )

    def pay(self):
        """pay by omise"""
        if self.user.status == self.Status_choice.UNPAID:
            source = omise.Source.create(
            type=self.payment_type,
            amount=self.bill.calculate_price(self.user)*100,
            currency="thb",
        )

            omise.api_secret = self.user.chain.key

            charge = omise.Charge.create(
                amount=int(self.bill.calculate_price(self.user) * 100),
                currency="thb",
                customer=self.user.chain_key,
                source=source.id,
                return_uri="http://localhost:8000/bill/",
            )
            self.charge_id = charge.id

            self.user.status = self.Status_choice.PAID
            self.user.save()
            omise.api_secret = OMISE_SECRET

    def get_status(self):
        status = omise.Charge.retrieve(self.charge_id).status
        if status == "successful":
            self.status = self.Status_choice.PAID
        elif status == "pending":
            self.status = self.Status_choice.PENDING
        else:
            self.status = self.Status_choice.UNPAID
        self.save()
        return super().get_status()

    def __repr__(self) -> str:
        return f"{super().__repr__()[:-1]} Paid by {self.payment_type})"


class CashPayment(BasePayment):
    def pay(self):
        if self.status == self.Status_choice.PAID:
            return 'Already paid'

        self.status = self.Status_choice.PAID
