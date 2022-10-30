from typing import Any
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Bills, Topic, UserProfile
from WePay.models.upload import UploadTopicForm


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


class CreateView(LoginRequiredMixin, generic.DetailView):
    """views for create some bills."""

    template_name = "Wepay/create_bills.html"
    model = Bills

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.POST:
            form = UploadTopicForm(request.POST, request.POST, request.POST,  request.POST)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(reverse("bills:bill"))
        return render(request, "Wepay/create_bills.html", {'form': UploadTopicForm})


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

# @login_required(login_url='accounts/login')
# def add_topics(request, bills_id):
#     bill = get_object_or_404(Bills, pk=bills_id)
#     user = request.user
#     return HttpResponseRedirect(reverse('bills:bill', args=(bill.id)))

# @login_required(login_url='accounts/login')
# def add_user(request, user_id):
#     pass
