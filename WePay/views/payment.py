from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import get_object_or_404, render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from ..models import Payment, omise
from django.db.models import QuerySet
from ..config import OMISE_SECRET


class PaymentView(LoginRequiredMixin, generic.ListView):
    """views for payment of each bill."""

    template_name = "Wepay/payment.html"
    context_object_name = "my_payment"

    def get_queryset(self) -> QuerySet:
        return Payment.objects.filter(
            user__user=self.request.user  # , status=Payment.Status_choice.UNPAID
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
        if payment.amount <= 20 or payment.amount > 150000:
            messages.info(
                request,
                "Your amount is less than 20 Baht or more than 150,000 Baht, you can only pay with cash",
            )
            cash_only = True

        if not payment.bill.header.chain:
            messages.info(
                request,
                "This bill is not in chain, you can only pay with cash or tell header to register the chain \
                    \n<a href='https://dashboard.omise.co/chain/authorize/pkey_test_5tgganhu45npoycv190'>instruction here</a>",
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
    payment.pay()
    print(omise.api_secret)
    omise.api_secret = OMISE_SECRET
    print("after: ", omise.api_secret)
    return HttpResponseRedirect(reverse("payments:payment"))
