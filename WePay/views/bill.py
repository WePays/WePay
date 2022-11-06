from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views import generic

from ..models import Bills, Payment, Topic, UserProfile


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


class BillCreateView(LoginRequiredMixin, generic.DetailView):
    template_name = "Wepay/create_bills.html"
    model = Bills

    def get(self, request, *args, **kwargs):
        user = request.user
        header = UserProfile.objects.get(user=user)
        lst_user = UserProfile.objects.exclude(user=user)
        # get all user of the bills by calling bills.all_user
        return render(
            request, self.template_name, {"header": header, "lst_user": lst_user}
        )

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            name = request.POST["title"]
            header = UserProfile.objects.get(user=user)
        except:
            messages.error(request, "Please fill all field of form")
        else:
            bill = Bills.objects.create(name=name, header=header)
            for user in bill.all_user:
                each_user_payment = Payment.objects.create(user=user, bill=bill)
                each_user_payment.save()
            bill.save()

            return HttpResponseRedirect(reverse("bills:bill"))
        return super(BillCreateView, self).post()


class DetailView(LoginRequiredMixin, generic.DetailView):
    """views for detail of each bill."""

    template_name = "Wepay/detail.html"
    model = Bills, Topic

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = request.user
        pk: int = kwargs["pk"]

        try:
            bill = Bills.objects.get(pk=pk, header__user=user)
        except Bills.DoesNotExist:
            messages.error(request, "Bill dosen't exist")
            return HttpResponseRedirect(reverse("bills:bill"))
        return render(request, "Wepay/detail.html", {"bill": bill})
