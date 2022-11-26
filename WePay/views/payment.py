from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import Http404, HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views import generic

from ..models import CashPayment, OmisePayment, Payment, PromptPayPayment


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
        try:
            payment = get_object_or_404(Payment, pk=kwargs["pk"], user__user=user)
        except Http404:
            messages.error(
                request, "Payment not found"
            )  # !BUG IT DOESNT COMING WHEN REDIRECT
            return HttpResponseRedirect(reverse("payments:payment"))
        status = payment.status
        payment_type = payment.payment_type
        if payment.price <= 20 or payment.price > 150000:
            messages.info(
                request,
                "* Your amount is less than 20 Baht or more than 150,000 Baht, you can only pay with cash",
            )
            cash_only = True

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

    def post(self, request, *args, **kwargs):
        """to be implement"""

        user = request.user
        payment = Payment.objects.get(pk=kwargs["pk"], user__user=user)
        payment_type = request.POST["payment_type"]
        payment.payment_type = payment_type
        print(payment_type)

        payment.save()
        payment.pay()
        if payment_type == "Cash":
            return HttpResponseRedirect(reverse("payments:payment"))
        if payment_type == "PromptPay":
            return HttpResponseRedirect(reverse("payments:qr", kwargs={"pk": payment.id}))

        return HttpResponseRedirect(payment.uri)


class QRViews(LoginRequiredMixin, generic.DetailView):
    template_name: str = "Wepay/qr.html"
    Model = Payment

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """get everything to choose payment type"""
        user = request.user
        try:
            payment = get_object_or_404(Payment, pk=kwargs["pk"], user__user=user)
        except Http404:
            messages.error(
                request, "Payment not found"
            )
            return HttpResponseRedirect(reverse("payments:payment"))

        if payment.payment_type != "PromptPay":
            messages.error(
                request, "Payment not found"
            )
            return HttpResponseRedirect(reverse("payments:payment"))

        return render(
            request,
            self.template_name,
            {
                "payment": payment,
            },
        )



def update(request, pk: int, *arg, **kwargs):
    user = request.user
    try:
        payment = get_object_or_404(Payment, pk=pk, user__user=user)
    except Http404:
        messages.error(request, "Payment not found")
        return HttpResponseRedirect(reverse("payments:payment"))
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

        plain_message = strip_tags(html_message)

        send_mail(
            subject="Someone Pay you a money",
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[header_mail],
            html_message=html_message,
        )

        if payment.bill.status:  # this mean bills is ready to verify and close
            # send mail to header to verify and close the bill
            html_message_to_header = render_to_string(
                "message/header/mail_to_header.html",
                {
                    "bill_name": payment.bill.name,
                },
            )

            plain_message_to_header = strip_tags(html_message_to_header)

            send_mail(
                subject="You have to verify and close the bill",
                message=plain_message_to_header,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[header_mail],
                html_message=html_message_to_header,
            )

    return HttpResponseRedirect(reverse("payments:payment"))


def confirm_payment(request, pk: int, *arg, **kwargs):
    try:
        payment = get_object_or_404(Payment, pk=pk)
    except Http404:
        messages.error(request, "Payment not found")
        return HttpResponseRedirect(reverse("payments:payment"))
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


def reset(request, pk: int, *arg, **kwargs):
    try:
        payment = get_object_or_404(Payment, pk=pk)
    except Http404:
        messages.error(request, "Payment not found")
        return HttpResponseRedirect(reverse("payments:payment"))
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


def reject(request, pk: int, *arg, **kwargs):
    # cash payment only

    try:
        payment = get_object_or_404(Payment, pk=pk)
    except Http404:
        messages.error(request, "Payment not found")
        return HttpResponseRedirect(request.path)
    if not isinstance(payment.instance, CashPayment):
        messages.error(request, "Payment is not rejectable")
        return HttpResponseRedirect(reverse("bills:detail", args=[payment.bill.id]))
    payment.instance.reject()
    payment.save()
    messages.success(request, "Payment is rejected")

    return HttpResponseRedirect(reverse("bills:detail", args=[payment.bill.id]))
