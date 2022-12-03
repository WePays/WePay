from typing import Tuple

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseNotFound,
)
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic

from ..models import Bills, OmisePayment, Payment, Topic, UserProfile
from ..utils.mailing import send_email


# def get_bill(pk: int, header: User) -> Tuple[Bills, HttpResponse]:
#     """get the bill

#     Arguments:
#         pk {int} -- id of that bill
#         header {User} -- bill's header

#     Returns:
#         Tuple[Bills, HttpResponse] -- that bill and response if bill not found
#     """
#     try:
#         bill = Bills.objects.get(pk=pk, header__user=header)
#     except Bills.DoesNotExist:
#         return None, HttpResponseNotFound("This bill doesnt exists")
#     return bill, None


class BillView(LoginRequiredMixin, generic.DetailView):
    """Display a list of bill and create userProfile if user dont have it before

    **Context**

    ``created_bill``
        A list of :model:`WePay.Bills` that is created

    ``Uncreated_bill``
        an instance of :model:`WePay.Bills` that havent created(but initailized)

    **Template:**

    :template:`WePay/bill.html`
    """

    template_name = "Wepay/bill.html"

    def get(self, request: HttpRequest, *arg, **kwargs) -> HttpResponse:
        """create a UserProfile object if User doesnt have
        and display a list of bill
        """
        # get a user
        user = request.user
        # check whether userprofile is created or not,
        # if not it will create a UserProfile for that user
        if not UserProfile.objects.filter(user_id=user.id).exists():
            UserProfile.objects.create(user_id=user.id)

        # get a list of bills that is created that ordering ny pubdate of bill
        created_bill_lst = Bills.objects.filter(
            header__user=request.user, is_created=True, is_closed=False
        ).order_by("-pub_date")

        try:  # get the last uncreated bill
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
        """Create a Bill object and redirect to bill page

        **messages**
        :error: if user initialized a bill before and not created it

        """
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
    """Page for Initialize :model:`WePay.Bills`

    **Context**

    ``header``
        an instance of :model:`WePay.UserProfile` that is the header of the bill(user)

    ``lst_user``
        list of all user in the application


    **Template:**

    :template:`WePay/create_bills.html`

    """

    template_name = "Wepay/create_bills.html"
    model = Bills

    def get(self, request, *args, **kwargs):
        """get everything that ready to be displayed in the page
        if it has uncreated bill it will redirect to Bills Page
        """
        user = request.user
        header = UserProfile.objects.get(user=user)
        lst_user = UserProfile.objects.all()

        uncreated_bill = Bills.objects.filter(header__user=user, is_created=False)
        if uncreated_bill:
            return redirect("/")

        return render(
            request, self.template_name, {"header": header, "lst_user": lst_user}
        )

    def post(self, request, *args, **kwargs):
        """Initialize a bill and redirect to add topic page"""
        # get all component from user input
        user = request.user
        name = request.POST["title"]
        topic_name = request.POST["topic_name"]
        topic_user = request.POST.getlist("username[]")
        topic_price = request.POST["topic_price"]
        header = UserProfile.objects.get(user=user)

        # initialize a bill
        bill = Bills.objects.create(name=name, header=header)
        topic = Topic.objects.create(title=topic_name, price=topic_price, bill=bill)
        for each_user in topic_user:
            user = UserProfile.objects.get(user__username=each_user)
            topic.add_user(user)
        bill.add_topic(topic)
        bill.save()

        return HttpResponseRedirect(f"/bill/{bill.id}/add")


class DetailView(LoginRequiredMixin, generic.DetailView):
    """Display a detail of a bill

    **Context**

    ``bill``
        an instance of :model:`WePay.Bills` that is that bil

    ``payment``
        list of each user payment (:model:`WePay.Payment`)

    **Template:**

    :template:`WePay/bill_detail.html`

    """

    template_name = "Wepay/detail.html"
    model = Bills, Topic

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """get each bill detail"""

        pk: int = kwargs["pk"]

        bill = get_object_or_404(Bills, pk=pk, header__user=request.user)
        # get all payment in that bill
        lst = []
        for each_user in bill.all_user:
            payment = Payment.objects.get(bill=bill, user=each_user)
            if (  # update status of OmisePayment if it in PENDING status
                isinstance(payment.instance, OmisePayment)
                and payment.status == Payment.Status_choice.PENDING
            ):
                payment.update_status()
            lst.append(payment)
        return render(request, "Wepay/detail.html", {"bill": bill, "payment": lst})


@login_required(login_url="/accounts/login/")
def create(request: HttpRequest, pk: int) -> HttpResponse:
    """create a bill that Initialized and send email notification
    to all user in that bill

    Arguments:
        pk {int} -- id of each bill

    **Context**

    render when send mail
    ``user``
        an instance of :model:`WePay.UserProfile` that is each user in the bill

    ``bill``
        name of that bill

    ``header``
        instance of :model:`WePay.UserProfile` that is header of bill

    ``price``
        price that each user need to pay

    ``topic``
        all topic in that bill
        (maybe refactor to topic that each user in that)

    **Template**

    :template:`message/user/assigned_bill.html`

    """

    bill = get_object_or_404(Bills, pk=pk, header__user=request.user)
    # if user assign bill to himself and only one it will thow a error message
    # and redirect to add topic page as usual

    if len(bill.all_user) == 1 and bill.all_user[0].user == request.user:
        messages.error(request, "You can't create a bill with only yourself")
        return HttpResponseRedirect(f"/bill/{bill.id}/add")
    # set bill to created
    bill.is_created = True

    # assigin each payment to user and send email notification
    for user in bill.all_user:
        each_user_payment = Payment.objects.create(user=user, bill=bill)
        if user == bill.header:  # header is alway paid
            each_user_payment.status = Payment.Status_choice.PAID
        each_user_payment.save()

        if user != bill.header:
            html_message_to_user = render_to_string(
                "message/user/assigned_bill.html",
                {
                    "user": user.user.username,
                    "bill": bill.name,
                    "header": bill.header.name,
                    "price": bill.total_price,
                    "topic": bill.topic_set.all(),
                },
            )

            send_email(
                subject="You got assign to a bill",
                html_message=html_message_to_user,
                recipient_list=[user.user.email],
            )

    bill.save()

    return HttpResponseRedirect(reverse("bills:bill"))


@login_required(login_url="/accounts/login/")
def delete(request: HttpRequest, pk: int) -> HttpResponse:
    """delete a bill that requested

    Arguments:
        pk {int} -- id of each bill

    **Context**
    render when send mail

    ``bill_name``
        name for that bill

    """
    header = request.user

    bill = get_object_or_404(Bills, pk=pk, header__user=header)
    # if anyone is paid or in pending status except header it will cant delete
    any_one_pay = any(
        payment.status in (Payment.Status_choice.PAID, Payment.Status_choice.PENDING)
        for payment in bill.payments.all()
        if payment.user.user != header
    )
    if any_one_pay:
        messages.warning(
            request, "! You can\u00a0t delete this bill because someone has paid"
        )
        return HttpResponseRedirect(reverse("bills:bill"))
    name = bill.name

    # send notification to each user that this bill is deleted
    for user in bill.all_user:
        html_message_to_user = render_to_string(
            "message/user/deleted_bill.html",
            {
                "bill_name": name,
            },
        )

        send_email(
            subject="This bill is deleted.",
            html_message=html_message_to_user,
            recipient_list=[user.user.email],
        )

    bill.delete()
    messages.success(request, f"Bill:{name} deleted")
    return HttpResponseRedirect(reverse("bills:bill"))


@login_required(login_url="/accounts/login/")
def close(request: HttpRequest, pk: int) -> HttpResponse:
    """close the bill after header click verify button
    then send notification to all user that this bill is closed

    Arguments:
        pk {int} -- id of each bill

    """
    bill = get_object_or_404(Bills, pk=pk, header__user=request.user)
    bill.is_closed = True
    bill.save()

    for user in bill.all_user:

        html_message_to_user = render_to_string(
            "message/user/closed_bill.html",
            {
                "bill_name": bill.name,
            },
        )

        send_email(
            subject="This bill is closed.",
            html_message=html_message_to_user,
            recipient_list=[user.user.email],
        )

    return HttpResponseRedirect(reverse("bills:bill"))
