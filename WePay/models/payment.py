# from django.contrib import admin
from abc import abstractmethod
from typing import Any

import omise
from django.db import models
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings

from .bill import Bills
from .userprofile import UserProfile
from ..config import OMISE_PUBLIC, OMISE_SECRET

omise.api_public = OMISE_PUBLIC
omise.api_secret = OMISE_SECRET


class Payment(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True
    )
    date = models.DateTimeField(
        null=True,
        blank=True,
        default=timezone.localtime().strftime(r"%Y-%m-%d %H:%M:%S"),
    )
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE, related_name="payments")
    uri = models.CharField(max_length=100, null=True, blank=True)

    class Status_choice(models.TextChoices):
        """choice for status whether PAID, PENDING, or UNPAID"""

        PAID = "PAID"
        PENDING = "PENDING"
        UNPAID = "UNPAID"
        FAIL = "FAIL"
        EXPIRED = "EXPIRED"

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
    def price(self):
        """get price of each payment"""
        return self.bill.calculate_price(self.user)

    @property
    def amount(self) -> int:
        """get amount of each payment"""
        if self.payment_type == self.PaymentChoice.CASH:
            return int(self.price)
        return int(self.price * 100)

    @property
    def selected_payment(self) -> Any:
        """get now payment"""
        return self.payment_dct[self.payment_type]

    @property
    def instance(self):
        selected = self.selected_payment
        if selected == CashPayment:
            return self.cashpayment.first()
        if selected == PromptPayPayment:
            return self.promptpaypayment.first()
        if selected == SCBPayment:
            return self.scbpayment.first()
        if selected == KTBPayment:
            return self.ktbpayment.first()
        if selected == BAYPayment:
            return self.baypayment.first()
        if selected == BBLPayment:
            return self.bblpayment.first()

    def can_pay(self) -> bool:
        return self.status == self.Status_choice.UNPAID

    def is_repayable(self) -> bool:
        return self.status in (self.Status_choice.FAIL, self.Status_choice.EXPIRED)

    def pay(self) -> None:
        """Pay to header"""
        if not self.can_pay():
            raise AlreadyPayError("You are in PENDING or PAID Status")

        now_payment = self.selected_payment.objects.get_or_create(payment=self)[0]
        now_payment.pay()
        self.save()

    def is_confirmable(self) -> bool:
        return self.status == self.Status_choice.PENDING and self.selected_payment in (
            CashPayment,
            PromptPayPayment,
        )

    # def update_status(self):
    #     omise.api_secret = self.payment.header.chain.key
    #     charge = omise.Charge.retrieve(self.charge_id)
    #     if charge:
    #         status = charge.status
    #         if status == "successful":
    #             self.payment.status = self.payment.Status_choice.PAID
    #         elif status == "pending":
    #             self.payment.status = self.payment.Status_choice.PENDING
    #     else:
    #         self.payment.status = self.payment.Status_choice.UNPAID
    #     self.payment.save()
    #     omise.api_secret = OMISE_SECRET
    #     self.save()

    def __repr__(self) -> str:
        """represent a payment"""
        return f"Payment(user={self.user}, date={self.date}, bill={self.bill}, status={self.status}, payment_type={self.payment_type})"

    __str__ = __repr__


class BasePayment(models.Model):
    """Entry model"""

    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, default=None, related_name="%(class)s"
    )

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

    class Meta:
        abstract = True

    def pay(self):
        """pay by omise"""
        print(self.payment.status)
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
            self.save()

    def update_status(self):  # TODO: Move this mothod to Payment class
        omise.api_secret = self.payment.header.chain.key
        charge = omise.Charge.retrieve(self.charge_id)
        if charge:
            status = charge.status
            if status == "successful":
                self.payment.status = self.payment.Status_choice.PAID
            elif status == "pending":
                self.payment.status = self.payment.Status_choice.PENDING
            elif status == "failed":
                self.payment.status = self.payment.Status_choice.FAIL
            elif status == "expired":
                self.payment.status = self.payment.Status_choice.EXPIRED

        else:
            self.payment.status = self.payment.Status_choice.UNPAID
        self.payment.save()
        omise.api_secret = OMISE_SECRET
        self.save()

    def reset(self):
        self.payment.status = self.payment.Status_choice.UNPAID
        self.charge_id = ""
        self.payment.uri = ""
        self.payment_type = "promptpay"
        self.payment.save()
        self.save()

    @property
    def payment_link(self) -> str:
        if self.charge_id:
            return f"https://dashboard.omise.co/test/charges/{self.charge_id}"
        return ""


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
    def confirm(self):
        if self.payment.status in (
            self.payment.Status_choice.PAID,
            self.payment.Status_choice.UNPAID,
        ):
            return

        self.payment.status = self.payment.Status_choice.PAID
        self.payment.save()

    def pay(self):

        print(self)
        if self.payment.status == self.payment.Status_choice.PAID:
            return

        # this will send notification to header to confirm
        self.payment.status = self.payment.Status_choice.PENDING
        self.payment.save()
        self.save()

        html_message_to_user = render_to_string(
            "message/header/mail_to_header.html",
            {
                "user": self.payment.user,
                "bill": self.payment.bill.name,
                "header": self.payment.bill.header.name,
                "price": self.payment.bill.total_price,
                "topic": self.payment.bill.topic_set.all(),
            },
        )

        plain_message_to_user = strip_tags(html_message_to_user)

        send_mail(
            subject="You got assign to a bill",
            message=plain_message_to_user,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.payment.user.user.email],
            html_message=html_message_to_user,
        )

    def reject(self):
        if self.payment.status == self.payment.Status_choice.PAID:
            return

        self.payment.status = self.payment.Status_choice.FAIL
        self.payment.save()

    def reset(self):
        # TODO: send message to user that you rejected this pls pay again
        self.payment.status = self.payment.Status_choice.UNPAID
        self.payment.save()


class AlreadyPayError(Exception):
    "This payment already paid"
