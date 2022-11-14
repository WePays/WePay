from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import get_object_or_404, render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from ..models import Payment, omise, SCBPayment, PromptPayPayment, BAYPayment, BBLPayment, KTBPayment
from django.db.models import QuerySet
from ..config import OMISE_SECRET


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
        print(status)
        payment_type = payment.payment_type
        if payment.price <= 20 or payment.price > 150000:
            messages.info(
                request,
                "Your amount is less than 20 Baht or more than 150,000 Baht, you can only pay with cash",
            )
            cash_only = True

        if not payment.bill.header.chain:
            messages.info(
                request,
                "This bill is not in chain, you can only pay with cash or tell header to register the chain \
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
    except Payment.DoesNotExist:
        messages.error(request, "Payment not found")
        return HttpResponseRedirect(reverse("payments:payment"))
    # payment.pay()
    payment_type = payment.selected_payment
    print(omise.api_secret)
    if payment_type == SCBPayment:
        payment_type = SCBPayment.objects.get(payment=payment)
        payment_type.update_status()
    elif payment_type == PromptPayPayment:
        payment_type = PromptPayPayment.objects.get(payment=payment)
        payment_type.update_status()
    elif payment_type == BAYPayment:
        payment_type = BAYPayment.objects.get(payment=payment)
        payment_type.update_status()
    elif payment_type == BBLPayment:
        payment_type = BBLPayment.objects.get(payment=payment)
        payment_type.update_status()
    elif payment_type == KTBPayment:
        payment_type = KTBPayment.objects.get(payment=payment)
        payment_type.update_status()
    print(omise.api_secret)
    print(payment.status)
    return HttpResponseRedirect(reverse("payments:payment"))
