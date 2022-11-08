from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from ..models import Payment
from django.db.models import QuerySet


class PaymentView(LoginRequiredMixin, generic.ListView):
    """views for payment of each bill."""

    template_name = "Wepay/payment.html"
    context_object_name = "my_payment"

    def get_queryset(self) -> QuerySet:
        return Payment.objects.filter(
            user__user=self.request.user, status=Payment.Status_choice.UNPAID
        )


class PaymentDetailView(LoginRequiredMixin, generic.DetailView):
    """views for payment detail of each bill."""

    template_name = "Wepay/payment_detail.html"
    Model = Payment

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            payment = get_object_or_404(Payment, pk=kwargs["pk"], user__user=user)
        except Payment.DoesNotExist:
            messages.error(request, "Payment not found")
            return redirect("payments:payment")
        status = payment.status
        payment_type = payment.payment_type
        return render(
            request,
            self.template_name,
            {"payment": payment, "status": status, "payment_type": payment_type}
        )

    def post(self, request, *args, **kwargs):
        """to be implement"""
        return
