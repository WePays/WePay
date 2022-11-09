from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import get_object_or_404, render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from ..models import Payment
from django.db.models import QuerySet


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
                "This bill is not in chain, you can only pay with cash or tell header to register the chain"
                # TODO: put the omise link here
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
        print(payment)
        print(payment.uri)
        return HttpResponseRedirect(payment.uri)
