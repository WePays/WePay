# from django.shortcuts import render
# from typing import Any
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Bills, Food  # , Food, BankPayment, CashPayment, PromptPayPayment

# from django.http import HttpRequest, HttpResponse
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
    model = Food

    def get(self, request):
        user = request.user
        return render(request, 'Wepay/create_bills.html')

def payment(request):
    return HttpResponse('<h1>payments</h1>')
