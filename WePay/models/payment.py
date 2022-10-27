# from django.contrib import admin
from abc import abstractmethod
from typing import Any
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .bill import Bills


class BasePayment(models.Model):
    """Entry model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.localtime)
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE)

    @abstractmethod
    def pay(self):
        pass

    class Status_choice(models.TextChoices):
        PAID = "PAID"
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

    @property
    def header(self):
        return self.bill.header

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(user={self.user}, date={self.date},\
    bill={self.bill}, status={self.status})"


class OmisePayment(BasePayment):
    class Meta:
        abstract = True

    def pay(self):
        pass


class BankPayment(OmisePayment):
    bank_account = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    class Bank_choice(models.TextChoices):
        KTB = "KTB"
        BBL = "BBL"
        SCB = "SCB"
        KRUNGTHAI = "KRUNGTHAI"
        TMB = "TTB"
        BAY = "BAY"
        REDCIT = "CREDIT"
        PROMPTPAY = "PROMPTPAY"
        other = "other"

    bank_name = models.CharField(
        choices=Bank_choice.choices, default=Bank_choice.other, max_length=10
    )

    def __repr__(self) -> str:
        return f"{super().__repr__()[:-1]} Paid by {self.Bank_choice})"


class PromptPayPayment(OmisePayment):
    phone_number = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __repr__(self) -> str:
        return f"{super().__repr__()[:-1]}PhoneNumber={self.phone_number})"


class CashPayment(BasePayment):
    # image = models.NOT_PROVIDED
    pass
