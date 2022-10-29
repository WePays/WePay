from typing import Any
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Bills, Topic, UserProfile  # , Food, BankPayment, CashPayment, PromptPayPayment

# from django.db import models


class BillView(LoginRequiredMixin, generic.ListView):
    """views for bill.html"""

    template_name = "Wepay/bill.html"
    context_object_name = "my_bill"

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not UserProfile.objects.filter(user_id=user.id).exists():
            UserProfile.objects.create(user_id=user.id)
        return render(request, self.template_name)

    def get_queryset(self):

        return Bills.objects.filter(header=request.user).order_by("-pub_date")


class CreateView(LoginRequiredMixin, generic.DetailView):
    """views for create some bills."""

    template_name = "Wepay/create_bills.html"
    model = Bills

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return render(request, "Wepay/create_bills.html")


class DetailView(LoginRequiredMixin, generic.DetailView):
    """views for detail of each bill."""

    template_name = "Wepay/detail.html"
    model = Bills, Topic

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        # user = request.user
        try:
            bills = Bills.objects.get(pk=pk)
        except Bills.DoesNotExist:
            messages.error(request, "Bill dosen't exist")
            return HttpResponseRedirect(reverse("bills:bill"))
        return render(request, "Wepay/detail.html", {"bills": bills})


def payment(request: HttpRequest):
    return HttpResponse("<h1>payments</h1>")

def add_topics(request):
    pass