# from django.contrib import admin
from abc import abstractmethod
from typing import Any

import omise
from django.db import models
from django.utils import timezone
# from polymorphic.admin import StackedPolymorphicInline, PolymorphicInlineSupportMixin

from .bill import Bills
from .userprofile import UserProfile

OMISE_PUBLIC = 'pkey_test_5tgganhu45npoycv190'
OMISE_SECRET = 'skey_test_5tecjczxmlxrbtfxhw9'

omise.api_public = OMISE_PUBLIC
omise.api_secret = OMISE_SECRET


class Payment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE)

    class Status_choice(models.TextChoices):
        PAID = "PAID"
        PENDING = 'PENDING'
        UNPAID = "UNPAID"

    status = models.CharField(
        choices=Status_choice.choices, default=Status_choice.UNPAID, max_length=10
    )

    class PaymentChoice(models.TextChoices):
        CASH = 'Cash'
        PROMPTPAY = 'PromptPay'
        SCB = 'SCB'
        KTB = 'KTB'
        BAY = 'BAY'
        CREDIT = 'Credit'

    payment_type = models.CharField(
        choices=PaymentChoice.choices, default=PaymentChoice.CASH, max_length=10
    )

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

    def pay(self):
        payment_dct = {'Cash': CashPayment, 'PromptPay': PromptPayPayment,
                       'SCB': SCBPayment, 'KTB': KTBPayment, 'BAY': BAYPayment}
        if self.status in (self.Status_choice.PAID, self.Status_choice.PENDING):
            return
        now_payment = payment_dct[self.payment_type].objects.create(payment=self)
        now_payment.pay()


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

    # def __repr__(self) -> str:
    #     return f"{self.__class__.__name__}(user={self.user}, date={self.date},\
    # bill={self.bill}, status={self.status})"


class OmisePayment(BasePayment):
    charge_id = models.CharField(max_length=100, null=True, blank=True)
    payment_type = models.CharField(max_length=100, default='promptpay')

    class Meta:
        abstract = True

    def pay(self):
        """pay by omise"""
        if self.payment.user.status == self.payment.Status_choice.UNPAID:
            source = omise.Source.create(
                type=self.payment_type,
                amount=self.payment.bill.calculate_price(self.user)*100,
                currency="thb",
            )

            omise.api_secret = self.payment.bill.header.chain.key

            charge = omise.Charge.create(
                amount=int(self.payment.bill.calculate_price(self.user) * 100),
                currency="thb",
                source=source.id,
                return_uri="http://localhost:8000/bill/",
            )
            self.charge_id = charge.id

            self.user.status = self.Status_choice.PAID
            self.user.save()
            omise.api_secret = OMISE_SECRET

    def get_status(self):  # TODO remove middle man
        status = omise.Charge.retrieve(self.charge_id).status
        if status == "successful":
            self.payment.status = self.payment.Status_choice.PAID
        elif status == "pending":
            self.payment.status = self.payment.Status_choice.PENDING
        else:
            self.payment.status = self.payment.Status_choice.UNPAID
        self.payment.save()
        self.save()
        return self.payment.status

    def __repr__(self) -> str:
        return f"{super().__repr__()[:-1]} Paid by {self.payment_type})"


class PromptPayPayment(OmisePayment):
    payment_type = "promptpay"

    def __repr__(self) -> str:
        return f"{super().__repr__()[:-1]} Paid by {self.payment_type})"


class SCBPayment(OmisePayment):
    payment_type = "internet_banking_scb"

    def __repr__(self) -> str:
        return f"{super().__repr__()[:-1]} Paid by {self.payment_type})"


class KTBPayment(OmisePayment):
    payment_type = "internet_banking_ktb"

    def __repr__(self) -> str:
        return f"{super().__repr__()[:-1]} Paid by {self.payment_type})"


class BBLPayment(OmisePayment):
    payment_type = "internet_banking_bbl"

    def __repr__(self) -> str:
        return f"{super().__repr__()[:-1]} Paid by {self.payment_type})"


class BAYPayment(OmisePayment):
    payment_type = "internet_banking_bay"

    def __repr__(self) -> str:
        return f"{super().__repr__()[:-1]} Paid by {self.payment_type})"


class CashPayment(BasePayment):
    def pay(self):
        if self.payment.status == self.payment.Status_choice.PAID:
            return

        self.payment.status = self.payment.Status_choice.PAID
        self.payment.save()
