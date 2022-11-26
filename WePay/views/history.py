from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpRequest

from ..models import Bills, Payment, UserProfile


class HistoryView(LoginRequiredMixin, generic.DetailView):
    """show history of payment and closed bill

    **context**

    ``bill_history``
        history of bill that verified and closed

    ``payment_history``
        history of payment that paid


    **Template:**

        :template:`WePay/history.html`

    """

    template_name = "Wepay/history.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """get a list of bill and payment history"""

        user = UserProfile.objects.get(user=request.user)
        bill_history = Bills.objects.filter(header=user, is_closed=True)
        payment_history = Payment.objects.filter(
            user=user, status=Payment.Status_choice.PAID
        )

        return render(
            request,
            self.template_name,
            {"bill_history": bill_history, "payment_history": payment_history},
        )
