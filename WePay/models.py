# from django.contrib import admin
from typing import List, Any
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import logging


class Bills(models.Model):
    header = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(default=timezone.localtime)

    class Meta:
        verbose_name = "Bill"
        verbose_name_plural = "Bills"

    def calculate_price(self, person: User) -> float:
        """calculate price for each person"""
        food = Food.objects.filter(bill=self)
        print(food[0].user.all())
        return sum(each_food.each_price() for each_food in food if person in each_food.user.all())

    @property
    def total_price(self):
        """calculate total price"""
        food = Food.objects.filter(bill=self)
        return sum(each_food.price for each_food in food)

    @property
    def all_user(self) -> List[User]:
        """return list of all user"""
        food = Food.objects.filter(bill=self)
        return list({each_food.user for each_food in food})

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
    user = models.ManyToManyField(User, related_name="food")

    def each_price(self):
        return self.price / len(self.user.all())

    def add_user(self, user):
        self.user.add(user)

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
        return f"{super().__repr__()[:-1]} Paid by {self.Bank_choice})"


class PromptPayPayment(OmisePayment):
    phone_number = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __repr__(self) -> str:
        return f"{super().__repr__()[:-1]}PhoneNumber={self.phone_number})"


class CashPayment(Payment):
    # image = models.NOT_PROVIDED
    pass
