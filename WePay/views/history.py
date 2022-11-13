from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import render
from ..models import Bills, Payment, UserProfile


class HistoryView(LoginRequiredMixin, generic.DetailView):
    template_name = "WePay/history.html"

    def get(self, request, *args, **kwargs):
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
