from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
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
