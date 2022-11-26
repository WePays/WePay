from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from ..models import Bills, Topic, UserProfile


class AddTopicView(LoginRequiredMixin, generic.DetailView):
    template_name: str = "Wepay/add_topic.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        bill = get_object_or_404(Bills, pk=kwargs["pk"], header__user=request.user)

        if bill.is_created:
            messages.warning(request, "Bill is created")
            return HttpResponseRedirect(reverse("bills:bill"))

        all_topic = Topic.objects.filter(bill=bill)
        lst_user = UserProfile.objects.all()
        return render(
            request,
            self.template_name,
            {"bill": bill, "all_topic": all_topic, "lst_user": lst_user},
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        bill = Bills.objects.get(pk=kwargs["pk"])
        topic_name = request.POST["topic_name"]
        topic_user = request.POST.getlist("username[]")
        topic_price = request.POST["topic_price"]
        topic = Topic.objects.create(
            title=topic_name, price=float(topic_price), bill=bill
        )

        for each_user in topic_user:
            user = UserProfile.objects.get(user__username=each_user)
            topic.add_user(user)

        return HttpResponseRedirect(reverse("bills:add", args=(bill.id,)))


def delete_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    bill = topic.bill
    if len(Topic.objects.filter(bill=bill)) == 1:
        messages.warning(request, "! Bill must have at least one topic")
        return HttpResponseRedirect(reverse("bills:add", args=(bill.id,)))
    topic.delete()
    return HttpResponseRedirect(reverse("bills:add", args=(bill.id,)))
