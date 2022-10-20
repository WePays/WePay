# from django.contrib import admin
from typing import List
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Bills(models.Model):
    header = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(default=timezone.localtime)

    class Meta:
        verbose_name = "Bill"
        verbose_name_plural = "Bills"

    def __repr__(self) -> str:
        return (
            f"Bills(header={self.header}, name={self.name}, pub_date={self.pub_date})"
        )

    __str__ = __repr__


class Food(models.Model):
    """Topic model"""

    title = models.CharField(max_length=100)
    price = models.IntegerField("price")
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE)
    user: List[User] = []

    def add_user(self, user):
        self.user.append(user)


class Payment(models.Model):
    """Entry model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE)

    class Status_choice(models.TextChoices):
        PAID = "PAID"
        UNPAID = "UNPAID"

    status = models.CharField(
        choices=Status_choice.choices, default=Status_choice.UNPAID, max_length=10
    )
    # image = models.ImageField(upload_to='images/', blank=True)

    class Meta:
        abstract = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(user={self.user}, date={self.date},\
    bill={self.bill}, status={self.status})"

    __str__ = __repr__


class OmisePayment(Payment):
    class Meta:
        abstract = True


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
        return super().__repr__()[:-1] + f" Paid by {self.Bank_choice})"


class PromptPayPayment(OmisePayment):
    phone_number = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + f"PhoneNumber={self.phone_number})"


class CashPayment(Payment):
    # image = models.NOT_PROVIDED
    pass
