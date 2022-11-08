from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from ..models import Bills, Topic, UserProfile


class AddTopicView(LoginRequiredMixin, generic.DetailView):
    template_name: str = "Wepay/add_topic.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        try:
            bill = get_object_or_404(Bills, pk=kwargs["pk"], header__user=request.user)
        except Bills.DoesNotExist:
            messages.warning(request, "Bill does not exist")
            return HttpResponseRedirect(reverse("bills:bill"))

        if bill.is_created:
            messages.warning(request, "Bill is created")
            return HttpResponseRedirect(reverse("bills:bill"))

        all_topic = Topic.objects.filter(bill=bill)
        lst_user = UserProfile.objects.all()
        return render(
            request, self.template_name, {"bill": bill, "all_topic": all_topic, "lst_user": lst_user}
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        bill = Bills.objects.get(pk=kwargs["pk"])
        topic_name = request.POST["topic_name"]
        topic_user = request.POST.getlist("username")
        topic_price = request.POST["topic_price"]
        topic = Topic.objects.create(
            title=topic_name, price=float(topic_price), bill=bill
        )

        for each_user in topic_user:
            user = UserProfile.objects.get(user__username=each_user)
            topic.add_user(user)

        return HttpResponseRedirect(reverse("bills:add", args=(bill.id,)))
