import os
from abc import abstractmethod
from urllib.request import urlretrieve
from typing import Any

import omise
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone

from .bill import Bills
from .userprofile import UserProfile
from ..utils import send_email

# set omise key
omise.api_public = settings.OMISE_PUBLIC
omise.api_secret = settings.OMISE_SECRET


class Payment(models.Model):
    """Payment for each person in each bill
    user -> :model:`Wepay.UserProfile` user for that bill
    date: date that those payment published
    bill -> :model:`WePay.Bills` bill of that payment
    """

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
        """choice for status whether PAID, PENDING, UNPAID, EXPIRED or FAILED"""

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
    def price(self) -> float:
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
    def instance(self) -> "BasePayment":
        """instance for each payment whether Cash, Promptpay, etc..

        Returns:
            BasePayment -- payment that user selected to pay with
        """
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
        """check whether that payment can pay or not

        Returns:
            bool -- True if payment status is UNPAID else False
        """
        return self.status == self.Status_choice.UNPAID

    def is_repayable(self) -> bool:
        """check whether that payment can repay or not

        Returns:
            bool -- True if payment is fail or expired
        """
        return self.status in (self.Status_choice.FAIL, self.Status_choice.EXPIRED)

    def pay(self) -> None:
        """Pay to header

        Raises:
            AlreadyPayError: if user repay and now payment status is pending or paid
        """
        # if payment cant pay it will raise error
        if not self.can_pay():
            raise AlreadyPayError("You are in PENDING or PAID Status")

        now_payment = self.selected_payment.objects.get_or_create(payment=self)[0]
        now_payment.pay()
        self.save()

    def is_confirmable(self) -> bool:
        """check whether payment is confirmable

        Returns:
            bool -- True is user pay with :model:`WePay.CashPayment` and :model:`WePay.PromptPaypayment` false otherwise
        """
        return self.status == self.Status_choice.PENDING and self.selected_payment in (
            CashPayment,
            PromptPayPayment,
        )

    def update_status(self) -> None:
        """update status of payment"""
        # id it is cash payment bypass it
        if isinstance(self.instance, CashPayment):
            return
        # change omise secret key to header chain key
        omise.api_secret = self.header.chain.key
        # if those payment is charged before it will check status
        charge = omise.Charge.retrieve(self.instance.charge_id)
        if charge:
            status = charge.status
            if status == "successful":
                self.status = self.Status_choice.PAID
            elif status == "pending":
                self.status = self.Status_choice.PENDING
            elif status == "failed":
                self.status = self.Status_choice.FAIL
            elif status == "expired":
                self.status = self.Status_choice.EXPIRED

        else:
            # it mean that the payent is unpaid otherwise
            self.status = self.Status_choice.UNPAID
        self.instance.save()
        omise.api_secret = settings.OMISE_SECRET
        self.save()

    def get_payment_data(self):
        """get the bill, user and date of this payment"""
        return self.bill, self.user, self.date, self.payment_type

    def delete(self, using=None, keep_parents=False):
        """delete payment and its instance"""
        if self.instance:
            self.instance.delete()
        super().delete(using, keep_parents)

    def __repr__(self) -> str:
        """represent a payment"""
        return f"Payment(user={self.user}, date={self.date}, bill={self.bill}, status={self.status}, payment_type={self.payment_type})"

    __str__ = __repr__


class BasePayment(models.Model):
    """Base class for EveryPayment
    it contain :model:`WePay.Payment` (Forign Key) (it is instance of Payment)
    """

    # related name = #(class)s mean that Payment class can use name of class to call this instance
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, default=None, related_name="%(class)s"
    )

    @abstractmethod
    def pay(self) -> None:
        """method for paying"""
        pass

    # make this class inheritable
    class Meta:
        abstract = True

    def __init_subclass__(cls) -> None:
        """make string method equal to represent method (magic method) if other inherited from this model"""
        super().__init_subclass__()
        cls.__str__ = cls.__repr__

    def __repr__(self) -> str:
        """represent object to classname status and user that link with this payment."""
        return f"{self.__class__.__name__}({self.payment.status}, {self.payment.user})"


class OmisePayment(BasePayment):
    """abstract model for paying through Promptpay and Internet Banking

    Attr:
        charge_id: id of each omise charge(if pay) to check status of each payment.
        payment_type: Omise payment type whether PromptPay, InternetBanking...
    """

    charge_id = models.CharField(max_length=100, null=True, blank=True)
    payment_type = models.CharField(max_length=100, default="promptpay")

    class Meta:
        abstract = True

    def pay(self) -> None:
        """pay by omise"""
        # amount must morethan 20
        if self.payment.status == self.payment.Status_choice.UNPAID:
            print(self.payment.amount)
            print(self.payment.price)
            print(self.payment.payment_type)
            source = omise.Source.create(
                type=self.payment_type,
                amount=self.payment.amount,
                currency="thb",
            )
            # change omise secret key to header's key
            omise.api_secret = self.payment.bill.header.chain.key
            # then make a charge
            charge = omise.Charge.create(
                amount=self.payment.amount,
                currency="thb",
                source=source.id,
                # return_uri=f"https:///wepays.herokuapp.com/payment/{self.payment.id}/update",
                return_uri=f"http:///127.0.0.1:8000/payment/{self.payment.id}/update",
            )
            # assign charge id  and uri to payment
            self.charge_id = charge.id
            self.payment.uri = charge.authorize_uri
            self.save()

    def reset(self) -> None:
        """reset a payment"""
        self.payment.status = self.payment.Status_choice.UNPAID
        self.charge_id = ""
        self.payment.uri = ""
        self.payment_type = "promptpay"
        self.payment.save()
        self.save()

    @property
    def payment_link(self) -> str:
        """get a payment link to header for update status via omise

        Returns:
            str -- uri of link to go to each charge
        """
        # id header has pay or mark as paud it will return a link to update srarus
        # it will return blank string otherwise
        if self.charge_id:
            return f"https://dashboard.omise.co/test/charges/{self.charge_id}"
        return ""


class PromptPayPayment(OmisePayment):
    """Inherited model from :model:`OmisePayment` that type is promptpay"""

    payment_type = "promptpay"

    @property
    def qr_name(self) -> str:
        """get qr name

        Returns:
            str -- qr name
        """
        return f"promptpay{self.payment.id}.svg"

    @property
    def qr_path(self) -> str:
        """get qr path for that payment

        Returns:
            str -- a full static path + {{qr name}}.svg
                ex. WePay/static/wepay/qr/promptpay5.svg
        """
        return f"WePay/static/wepay/qr/{self.qr_name}"

    def genetate_qr(self) -> None:
        """generate QR for prompytpay payment"""
        # check whether qr is in path or not,
        # if it exist it will exit the function
        if os.path.isfile(self.qr_path):
            return
        # if charge exist it will download the qr in to path
        if charge := omise.Charge.retrieve(self.charge_id):
            uri = charge.source.scannable_code.image.download_uri
            urlretrieve(uri, self.qr_path)

    def pay(self) -> None:
        """pay to header"""
        super().pay()
        self.genetate_qr()


class SCBPayment(OmisePayment):
    """Inherited model from :model:`OmisePayment` that type is Scb"""

    payment_type = "internet_banking_scb"


class KTBPayment(OmisePayment):
    """Inherited model from :model:`OmisePayment` that type is KTB"""

    payment_type = "internet_banking_ktb"


class BBLPayment(OmisePayment):
    """Inherited model from :model:`OmisePayment` that type is BBL"""

    payment_type = "internet_banking_bbl"


class BAYPayment(OmisePayment):
    """Inherited model from :model:`OmisePayment` that type is Bay"""

    payment_type = "internet_banking_bay"


class CashPayment(BasePayment):
    """Cash Payment for user to pay"""

    def confirm(self) -> None:
        """Confrom the payment when payment to header"""
        # it work when paymentstatus id pending
        if self.payment.status in (
            self.payment.Status_choice.PAID,
            self.payment.Status_choice.UNPAID,
        ):
            return

        self.payment.status = self.payment.Status_choice.PAID
        self.payment.save()

    def pay(self) -> None:
        """mark the status as paid and send mail to header to confirm this payment"""

        if self.payment.status == self.payment.Status_choice.PAID:
            return

        # this will send notification to header to confirm
        self.payment.status = self.payment.Status_choice.PENDING
        self.payment.save()
        self.save()

        html_message_to_header = render_to_string(
            "message/header/mail_to_header.html",
            {
                "user": self.payment.user,
                "bill": self.payment.bill.name,
                "header": self.payment.header.name,
                "price": self.payment.bill.total_price,
                "topic": self.payment.bill.topic_set.all(),
            },
        )

        send_email(
            subject="You got assign to a bill",
            html_message=html_message_to_header,
            recipient_list=[self.payment.user.user.email],
        )

    def reject(self) -> None:
        """this payment was rejecred and set it to FAIL status"""
        if self.payment.status == self.payment.Status_choice.PAID:
            return

        html_message = render_to_string(
            "message/user/rejected_bill.html",
            {
                "user": self.payment.user,
                "bill_title": self.payment.bill.name,
                "header": self.payment.header.name,
            },
        )

        send_email(
            subject=f"Your payment for {self.payment.bill.name} has been rejected",
            html_message=html_message,
            recipient_list=[self.payment.user.user.email],
        )

        self.payment.status = self.payment.Status_choice.FAIL
        self.payment.save()

    def reset(self) -> None:
        """reset the payment status"""
        self.payment.status = self.payment.Status_choice.UNPAID
        self.payment.save()


class AlreadyPayError(Exception):
    "This payment already paid"
