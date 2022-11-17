from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic

from ..models import Bills, Payment, Topic, UserProfile


class BillView(LoginRequiredMixin, generic.DetailView):
    """views for bill.html"""

    template_name = "Wepay/bill.html"

    def get(self, request, *arg, **kwargs):
        user = request.user
        if (
            user.is_authenticated
            and not UserProfile.objects.filter(user_id=user.id).exists()
        ):
            UserProfile.objects.create(user_id=user.id)

        created_bill_lst = Bills.objects.filter(
            header__user=request.user, is_created=True, is_closed=False
        ).order_by("-pub_date")
        try:
            uncreated_bill = Bills.objects.get(
                header__user=request.user, is_created=False
            )
        except Bills.DoesNotExist:
            uncreated_bill = None

        return render(
            request,
            self.template_name,
            {"created_bill": created_bill_lst, "uncreated_bill": uncreated_bill},
        )

    def post(self, request, *args, **kwargs):
        uncreated = Bills.objects.filter(
            header__user=request.user, is_created=False
        ).order_by("-pub_date")
        if uncreated:
            messages.error(
                request, "* You have an uncreated bill, please create it first"
            )
            return redirect("/")
        return HttpResponseRedirect(reverse("bills:create"))


class BillCreateView(LoginRequiredMixin, generic.DetailView):
    template_name = "Wepay/create_bills.html"
    model = Bills

    def get(self, request, *args, **kwargs):
        user = request.user
        header = UserProfile.objects.get(user=user)
        lst_user = UserProfile.objects.all()
        # get all user of the bills by calling bills.all_user

        uncreated_bill = Bills.objects.filter(header__user=user, is_created=False)
        if uncreated_bill:
            return redirect("/")

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
            messages.error(request, "! This bill dosen't exist")
            return HttpResponseRedirect(reverse("bills:bill"))
        lst = []
        for each_user in bill.all_user:
            payment = Payment.objects.get(bill=bill, user=each_user)
            lst.append(payment)
        return render(request, "Wepay/detail.html", {"bill": bill, "payment": lst})


@login_required(login_url="/accounts/login/")
def create(request: HttpRequest, pk: int):
    try:
        bill = Bills.objects.get(pk=pk)
    except Bills.DoesNotExist:
        messages.error(request, "! This Bill dosen't exist")
        return HttpResponseRedirect(reverse("bills:bill"))
    bill.is_created = True
    for user in bill.all_user:
        each_user_payment = Payment.objects.create(user=user, bill=bill)
        if user == bill.header:
            each_user_payment.status = Payment.Status_choice.PAID
        each_user_payment.save()
    bill.save()

    return HttpResponseRedirect(reverse("bills:bill"))


@login_required(login_url="/accounts/login/")
def delete(request: HttpRequest, pk: int):
    header = request.user
    try:
        bill = Bills.objects.get(pk=pk, header__user=header)
    except Bills.DoesNotExist:
        messages.error(request, "! This bill Bill dosen't exist")
        return HttpResponseRedirect(reverse("bills:bill"))
    any_one_pay = any(
        payment.status in (Payment.Status_choice.PAID, Payment.Status_choice.PENDING)
        for payment in bill.payments.all()
        if payment.user.user != header
    )
    if any_one_pay:
        messages.warning(request, "! You can't delete this bill because someone has paid")
        return HttpResponseRedirect(reverse("bills:bill"))
    name = bill.name
    bill.delete()
    messages.success(request, f"Bill:{name} deleted")
    return HttpResponseRedirect(reverse("bills:bill"))


@login_required(login_url="/accounts/login/")
def close(request: HttpRequest, pk: int):
    bill = Bills.objects.get(pk=pk)
    print(bill)
    bill.is_closed = True
    bill.save()
    return HttpResponseRedirect(reverse("bills:bill"))
