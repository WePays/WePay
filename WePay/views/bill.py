from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from ..models import Bills, Payment, Topic, UploadBillForm, UploadTopicForm, UserProfile


class BillView(LoginRequiredMixin, generic.ListView):
    """views for bill.html"""

    template_name = "Wepay/bill.html"
    context_object_name = "my_bill"

    def get(self, request, *arg, **kwargs):
        user = request.user
        if (
            user.is_authenticated
            and not UserProfile.objects.filter(user_id=user.id).exists()
        ):
            UserProfile.objects.create(user_id=user.id)
        return super().get(request, *arg, **kwargs)

    def get_queryset(self):

        return Bills.objects.filter(header__user=self.request.user).order_by(
            "-pub_date"
        )


class CreateView(LoginRequiredMixin, generic.DetailView):
    """views for create some bills."""

    template_name = "Wepay/create_bills.html"
    model = Bills

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        return render(
            request,
            "Wepay/create_bills.html",
            {"form_topic": UploadTopicForm, "form_bill": UploadBillForm},
        )

    def post(self, request, *args, **kwargs):
        user = request.user
        form_topic = UploadTopicForm(request.POST)
        # request.POST['bill']
        form_bill = UploadBillForm(request.POST)
        if form_topic.is_valid() and form_bill.is_valid():
            form_topic.save()
            form_bill.save(form_topic.instance)
            all_bill = Bills.objects.filter(header__user=user).last()
            for user in all_bill.all_user:
                each_user_payment = Payment.objects.create(user=user, bill=all_bill)
                each_user_payment.save()
        return HttpResponseRedirect(reverse("bills:bill"))


class DetailView(LoginRequiredMixin, generic.DetailView):
    """views for detail of each bill."""

    template_name = "Wepay/detail.html"
    model = Bills, Topic

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = request.user
        pk: int = kwargs["pk"]

        try:
            bill = Bills.objects.get(pk=pk, header__user=user)
        except Bill.DoesNotExist:
            messages.error(request, "Bill dosen't exist")
            return HttpResponseRedirect(reverse("bills:bill"))
        return render(request, "Wepay/detail.html", {"bill": bill})
