from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import get_object_or_404, render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from ..models import Bills, Payment, UserProfile
from django.db.models import QuerySet


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
