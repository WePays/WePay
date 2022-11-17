from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, reverse
from django.views import generic
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from ..config import OMISE_SECRET
from ..models import (
    BAYPayment,
    BBLPayment,
    KTBPayment,
    Payment,
    PromptPayPayment,
    SCBPayment,
    OmisePayment,
    CashPayment
)


class PaymentView(LoginRequiredMixin, generic.ListView):
    """views for payment of each bill."""

    template_name = "Wepay/payment.html"
    context_object_name = "my_payment"

    def get_queryset(self) -> QuerySet:
        return Payment.objects.filter(user__user=self.request.user).exclude(
            status=Payment.Status_choice.PAID
        )


class PaymentDetailView(LoginRequiredMixin, generic.DetailView):
    """views for payment detail of each bill."""

    template_name = "Wepay/payment_detail.html"
    Model = Payment

    def get(self, request, *args, **kwargs):
        user = request.user
        cash_only = False
        try:
            payment = get_object_or_404(Payment, pk=kwargs["pk"], user__user=user)
        except Payment.DoesNotExist:
            messages.error(request, "Payment not found")
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
                    \n<a href='/instruction/'>instruction here</a>",
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

        payment.pay()
        payment.save()
        if payment_type == "Cash":
            return HttpResponseRedirect(reverse("payments:payment"))
        # * after this will involked update status function
        return HttpResponseRedirect(payment.uri)


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
    payment.instance.update_status()
    header_mail = payment.bill.header.user.email
    html_message = render_to_string('message/header/someone_pay.html', {
                                    'user': payment.user, 'bill_name': payment.bill.name, 'payment_type': payment.instance.payment_type, 'price': payment.price, 'bill_id': payment.bill.id})
    plain_message = strip_tags(html_message)

    message = f'{payment.user} has paid Bill\'s {payment.bill.name}'
    message += f' with {payment.instance.payment_type}\n for {payment.price} Baht.'
    send_mail(
        subject='Someone Pay you a money',
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[header_mail],
        html_message=html_message
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
    payment.instance.reset()
    payment.save()

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
