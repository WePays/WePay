from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
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
        lst_user = UserProfile.objects.all()
        # get all user of the bills by calling bills.all_user
        return render(
            request, self.template_name, {"header": header, "lst_user": lst_user}
        )

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            name = request.POST["title"]
            topic_name = request.POST["topic_name"]
            topic_user = request.POST.getlist("username")
            topic_price = request.POST["topic_price"]
            header = UserProfile.objects.get(user=user)
        except Exception as e:
            messages.error(request, f"Error occured: {e}")
        else:
            bill = Bills.objects.create(name=name, header=header)
            topic = Topic.objects.create(title=topic_name, price=topic_price, bill=bill)

            for each_user in topic_user:

                user = UserProfile.objects.get(user__username=each_user)
                topic.add_user(user)
                bill.add_topic(topic)
            bill.save()

            return HttpResponseRedirect(f"/bill/{bill.id}/add")
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
        except Bills.DoesNotExist:
            messages.error(request, "Bill dosen't exist")
            return HttpResponseRedirect(reverse("bills:bill"))
        lst = []
        for each_user in bill.all_user:
            payment = Payment.objects.filter(bill=bill, user=each_user)
            print(payment, each_user)
            lst.append(payment)
        return render(request, "Wepay/detail.html", {"bill": bill, "payment":lst})


def create(request: HttpRequest, pk: int):
    bill = Bills.objects.get(pk=pk)
    bill.is_created = True

    for user in bill.all_user:
        each_user_payment = Payment.objects.create(user=user, bill=bill)
        each_user_payment.save()
    bill.save()

    return HttpResponseRedirect(reverse("bills:bill"))
