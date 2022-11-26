from typing import Tuple

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import Http404, HttpResponseRedirect, HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, reverse
from django.template.loader import render_to_string
from django.views import generic

from ..models import CashPayment, OmisePayment, Payment, PromptPayPayment
from ..utils import send_email


class PaymentView(LoginRequiredMixin, generic.ListView):
    """Display a list of all payment that each user need to pay

    **Context**

    ``my_payment``
        all user :model:`Payment` (need to pay)

    **Template:**

    :template:`Wepay/payment.html`
    """

    template_name = "Wepay/payment.html"
    context_object_name = "my_payment"

    def get_queryset(self) -> QuerySet:
        """get all user payment thst exclude PAID payment"""
        return Payment.objects.filter(user__user=self.request.user).exclude(
            status=Payment.Status_choice.PAID
        )


class PaymentDetailView(LoginRequiredMixin, generic.DetailView):
    """view for choosing payment and redirect to payment page

    **Context**

    ``payment``
        payment that user need to pay

    ``status``
        status of each payment

    ``payment_type``
        type of each payment

    ``cash_only``
        True if header not have OmiseChain
        or amout to pay is less than 20 baht or more than 150,000 baht.


    **Template**

    :template:`Wepay/payment_detail.html`
    """

    template_name = "Wepay/payment_detail.html"
    Model = Payment

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """get everything to choose payment type"""
        user = request.user
        cash_only = False

        payment = get_object_or_404(Payment, pk=kwargs["pk"], user__user=user)

        status = payment.status
        payment_type = payment.payment_type
        # payer cant pay with omise when price less than 20 or more than 150k Baht
        if payment.price <= 20 or payment.price > 150000:
            messages.info(
                request,
                "* Your amount is less than 20 Baht or more than 150,000 Baht, you can only pay with cash",
            )
            cash_only = True
        # payer must have chain to paid with omise
        if not payment.bill.header.chain:
            messages.info(
                request,
                "* This bill is not in chain, you can only pay with cash or tell header to register the chain \
                    \n instruction<a href='/instruction/'> here</a>",
                extra_tags="safe",
            )
            cash_only = True

        return render(
            request,
            self.template_name,
            {
                "payment": payment,
                "status": status,
                "payment_type": payment_type,
                "cash_only": cash_only,
            },
        )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Choose a payment type and pay to header"""

        user = request.user
        payment = get_object_or_404(Payment, pk=kwargs["pk"], user__user=user)
        payment_type = request.POST["payment_type"]
        payment.payment_type = payment_type

        payment.pay()
        payment.save()
        if payment_type == "Cash":
            return HttpResponseRedirect(reverse("payments:payment"))
        if payment_type == "PromptPay":
            return HttpResponseRedirect(
                reverse("payments:qr", kwargs={"pk": payment.id})
            )

        return HttpResponseRedirect(payment.uri)


class QRViews(LoginRequiredMixin, generic.DetailView):
    """QR-generator for PromptPay payment

    **Context**

    ``payment``
        payment that user need to pay

    **Template**

    :template:`Wepay/qr.html`

    """
    template_name: str = "Wepay/qr.html"
    Model = Payment

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """get everything to choose payment type"""
        user = request.user

        payment = get_object_or_404(Payment, pk=kwargs["pk"], user__user=user)

        if payment.payment_type != "PromptPay":
            messages.error(request, "Payment not found")
            return HttpResponseRedirect(reverse("payments:payment"))

        return render(
            request,
            self.template_name,
            {
                "payment": payment,
            },
        )


def update(request: HttpRequest, pk: int, *arg, **kwargs) -> HttpResponse:
    """update payment an OmisePaymentstatus

    Arguments:
        pk {int} -- id of each payment

    **Context**

    render when send mail
    ``user``
        an instance of :model:`WePay.UserProfile` that is each user in the bill

    ``bill_name``
        name of that bill

    ``payment_type``
        type of that payment

    ``price``
        price that each user need to pay

    ``bill_id``
        id of bill that link with that payment


    """
    user = request.user

    payment = get_object_or_404(Payment, pk=pk, user__user=user)
    payment_type = payment.selected_payment

    if not issubclass(payment_type, OmisePayment):
        messages.error(request, "Payment is not omise payment")
        return HttpResponseRedirect(reverse("payments:payment"))
    payment.update_status()
    header_mail = payment.bill.header.user.email

    if payment.status == Payment.Status_choice.PAID:

        html_message = render_to_string(
            "message/header/someone_pay.html",
            {
                "user": payment.user,
                "bill_name": payment.bill.name,
                "payment_type": payment.instance.payment_type,
                "price": payment.price,
                "bill_id": payment.bill.id,
            },
        )

        send_email(
            subject="Someone Pay you a money",
            html_message=html_message,
            recipient_list=[header_mail],
        )

        if payment.bill.status:  # this mean bills is ready to verify and close
            # send mail to header to verify and close the bill
            html_message_to_header = render_to_string(
                "message/header/mail_to_header.html",
                {
                    "bill_name": payment.bill.name,
                },
            )

            send_email(
                subject="You have to verify and close the bill",
                html_message=html_message_to_header,
                recipient_list=[header_mail],
            )

    return HttpResponseRedirect(reverse("payments:payment"))


def confirm_payment(request: HttpRequest, pk: int, *arg, **kwargs) -> HttpResponse:
    """confirm payment to payer when payer is paid

    Arguments:
        pk {int} -- id of each payment

    """
    payment = get_object_or_404(Payment, pk=pk)

    if not payment.is_confirmable():
        messages.error(request, "Payment is not comfirmable")
        return HttpResponseRedirect(
            reverse(
                "bills:detail",
                args=[
                    payment.bill.id,
                ],
            )
        )
    # if payer chose to pay with promptpay it will redirect to omise to confirm that you receive money
    if isinstance(payment.instance, PromptPayPayment):
        return HttpResponseRedirect(payment.instance.payment_link)
    payment.instance.confirm()
    payment.save()

    return HttpResponseRedirect(
        reverse(
            "bills:detail",
            args=[
                payment.bill.id,
            ],
        )
    )


def reset(request: HttpRequest, pk: int, *arg, **kwargs) -> HttpResponse:
    """reset payment to UNPAID status

    Arguments:
        pk {int} -- id of payment to reset

    Returns:
        HttpResponse -- _description_
    """
    payment = get_object_or_404(Payment, pk=pk)

    # if payment is fail or expired its mean it can repayable
    if not payment.is_repayable():
        messages.error(request, "Payment is not resetable")
        return HttpResponseRedirect(reverse("payments:payment"))
    bill, user, date, payment_type = payment.get_payment_data()
    payment.delete()
    new_payment = Payment.objects.create(
        user=user, bill=bill, date=date, payment_type=payment_type
    )
    new_payment.save()

    return HttpResponseRedirect(reverse("payments:payment"))


def reject(request: HttpRequest, pk: int, *arg, **kwargs) -> HttpResponse:
    """reject a payment for user

    Arguments:
        pk {int} -- id of payment to reject
    """

    payment = get_object_or_404(Payment, pk=pk)

    if not isinstance(payment.instance, CashPayment):
        messages.error(request, "Payment is not rejectable")
        return HttpResponseRedirect(reverse("bills:detail", args=[payment.bill.id]))
    payment.instance.reject()
    payment.save()
    messages.success(request, "Payment is rejected")

    return HttpResponseRedirect(reverse("bills:detail", args=[payment.bill.id]))
