# from django.shortcuts import render
# from typing import Any
from django.views import generic
from .models import Bills  # , Food, BankPayment, CashPayment, PromptPayPayment

# from django.http import HttpRequest, HttpResponse
# from django.db import models


# class BillView(generic.ListView):
#     """views for bill.html"""

#     template_name = "Wepay/bill.html"
#     context_object_name = "my_bill"

#     def get_queryset(self):
#         return Bills.objects.filter(header=self.request.user).order_by("-pub_date")
