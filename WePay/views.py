# from django.shortcuts import render
# from typing import Any
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import Bills, Food  # , Food, BankPayment, CashPayment, PromptPayPayment

# from django.http import HttpRequest, HttpResponse
# from django.db import models


# class BillView(generic.ListView):
#     """views for bill.html"""

#     template_name = "Wepay/bill.html"
#     context_object_name = "my_bill"

#     def get_queryset(self):
#         return Bills.objects.filter(header=self.request.user).order_by("-pub_date")

# class DetailBillView(generic.DetailView):
#     """Views for detail_bill"""
#     pass

# class CreateBillView(generic.DetailView):
#     """Views for create_bills"""
#     template_name = "Wepay/create_bills.html"
#     model = Food

#     return HttpResponse("")

def bill(request):
    return HttpResponse('<h1>Bill</h1>')

def create(request):
    return HttpResponse('<h1>create</h1>')

def detail(request):
    return HttpResponse('<h1>detail</h1>')
