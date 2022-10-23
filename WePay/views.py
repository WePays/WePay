from typing import Any
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Bills, Food  # , Food, BankPayment, CashPayment, PromptPayPayment

# from django.db import models


class BillView(LoginRequiredMixin, generic.ListView):
    """views for bill.html"""

    template_name = "Wepay/bill.html"
    context_object_name = "my_bill"

    def get_queryset(self):
        return Bills.objects.filter(header=self.request.user).order_by("-pub_date")


class CreateView(LoginRequiredMixin, generic.DetailView):
    """views for create some bills."""

    template_name = "Wepay/create_bills.html"
    model = Bills, Food

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return render(request, "Wepay/create_bills.html")


class DetailView(LoginRequiredMixin, generic.DetailView):
    """views for detail of each bill."""
    template_name = "Wepay/detail.html"
    model = Bills, Food

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        # user = request.user
        try:
            bills = Bills.objects.get(pk=pk)
        except Bills.DoesNotExist:
            messages.error(request, "Bill dosen't exist")
            return HttpResponseRedirect(reverse('bills:bill'))
        return render(request, "Wepay/detail.html", {'bills': bills})


def payment(request: HttpRequest):
    return HttpResponse("<h1>payments</h1>")
