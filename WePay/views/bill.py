from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
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


# class CreateView(LoginRequiredMixin, generic.CreateView):
#     """views for create some bills."""

#     template_name = "Wepay/create_bills.html"
#     model = Bills
#     form_class = UploadBillForm
#     success_url = reverse_lazy("bills:bill")

#     def get_form_kwargs(self):
#         print('HELLOOOOOOOOOOO')
#         kwargs = super(CreateView, self).get_form_kwargs()
#         kwargs.update({"request": self.request})
#         return kwargs

#     def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

#         return render(
#             request,
#             "Wepay/create_bills.html",
#             {"form_topic": UploadTopicForm, "form_bill": UploadBillForm},
#         )

#     def post(self, request, *args, **kwargs):
#         user = request.user
#         form_topic = UploadTopicForm(request.POST)
#         # request.POST['bill']
#         form_bill = UploadBillForm(request.POST)
#         if form_topic.is_valid() and form_bill.is_valid():
#             form_topic.save()
#             form_bill.save(form_topic.instance)
#             all_bill = Bills.objects.filter(header__user=user).last()
#             for user in all_bill.all_user:
#                 each_user_payment = Payment.objects.create(user=user, bill=all_bill)
#                 each_user_payment.save()
#         return HttpResponseRedirect(reverse("bills:bill"))

class BillCreateView(LoginRequiredMixin, generic.DetailView):
    template_name = "Wepay/create_bills.html"
    model = Bills

    def get(self, request, *args, **kwargs):
        user = request.user
        header = UserProfile.objects.get(user=user)
        # get all user of the bills by calling bills.all_user
        return render(request, self.template_name, {"header": header})

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            name = request.POST["title"]
            header = UserProfile.objects.get(user=user)
        except:
            messages.error(request, 'Please fill all field of form')
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
        except Bill.DoesNotExist:
            messages.error(request, "Bill dosen't exist")
            return HttpResponseRedirect(reverse("bills:bill"))
        return render(request, "Wepay/detail.html", {"bill": bill})
