from typing import Any
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet

from .models import Bills, Topic, UserProfile, UploadBillForm, UploadTopicForm, \
    CashPayment, PromptPayPayment, SCBPayment, KTBPayment, BBLPayment, BAYPayment


class BillView(LoginRequiredMixin, generic.ListView):
    """views for bill.html"""

    template_name = "Wepay/bill.html"
    context_object_name = "my_bill"

    def get(self, request, *arg, **kwargs):
        user = request.user
        if user.is_authenticated and not UserProfile.objects.filter(user_id=user.id).exists():
            UserProfile.objects.create(user_id=user.id)
        return super().get(request, *arg, **kwargs)

    def get_queryset(self):

        return Bills.objects.filter(header__user=self.request.user).order_by("-pub_date")


class AboutUsView(generic.TemplateView):
    """views for aboutus.html"""

    template_name = "Wepay/aboutus.html"


class CreateView(LoginRequiredMixin, generic.CreateView):
    """views for create some bills."""

    template_name = "Wepay/create_bills.html"
    model = UploadBillForm, UploadTopicForm
    fields = ("header", "name", 'title', 'price', 'bill', 'user')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return render(request, "Wepay/create_bills.html", {'form_topic': UploadTopicForm, 'form_bill': UploadBillForm})

    # def post(self, request, *args, **kwargs):
    #     form_topic = UploadTopicForm(request.POST)
    #     form_bill = UploadBillForm(request.POST)
    #     if form_topic.is_valid() and form_bill.is_valid():
    #         form_topic.save()
    #         form_bill.save()
    #     return HttpResponseRedirect(reverse("bills:bill"))


class AddTopicView(LoginRequiredMixin, generic.DetailView):
    """views for add topic to bills."""
    template_name = "Wepay/add_topic.html"
    model = Bills, Topic

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            bills = Bills.objects.get(pk=pk)
        except Bills.DoesNotExist:
            return HttpResponseRedirect(reverse("bills:bill"))
        return render(request, "Wepay/add_topic.html", {"bills": bills, 'form_topic': UploadTopicForm})

    def post(self, request, *args, **kwargs):
        form_topic = UploadTopicForm(request.POST)
        if form_topic.is_valid():
            form_topic.save()
        return HttpResponseRedirect(reverse("bills:bill"))


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


class PaymentView(LoginRequiredMixin, generic.ListView):
    """views for payment of each bill."""
    template_name = "Wepay/payment.html"
    context_object_name = "my_payment"

    def get_queryset(self) -> QuerySet:
        promptpay = PromptPayPayment.objects.filter(
            user__user=self.request.user, status=PromptPayPayment.Status_choice.UNPAID)
        scb = SCBPayment.objects.filter(user__user=self.request.user,
                                        status=SCBPayment.Status_choice.UNPAID)
        stb = KTBPayment.objects.filter(user__user=self.request.user,
                                        status=STBPayment.Status_choice.UNPAID)
        bbl = BBLPayment.objects.filter(user__user=self.request.user,
                                        status=BBLPayment.Status_choice.UNPAID)
        bay = BAYPayment.objects.filter(user__user=self.request.user,
                                        status=BAYPayment.Status_choice.UNPAID)
        cash = CashPayment.objects.filter(
            user__user=self.request.user, status=CashPayment.Status_choice.UNPAID)

        all_payment = promptpay | scb | stb | bbl | bay | cash
        return all_payment
