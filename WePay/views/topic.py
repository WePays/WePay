from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from ..models import Bills, Topic, UserProfile


class AddTopicView(LoginRequiredMixin, generic.DetailView):
    template_name: str = "Wepay/add_topic.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        print(kwargs['pk'])
        try:
            bill = get_object_or_404(Bills, pk=kwargs["pk"])
        except Bills.DoesNotExist:
            messages.warning(request, "Bill does not exist")
            return HttpResponseRedirect(reverse("bills:bill"))

        all_topic = Topic.objects.filter(bill=bill)
        lst_user = UserProfile.objects.all()
        return render(
            request, self.template_name, {"bill": bill, "all_topic": all_topic, "lst_user": lst_user}
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        bill = Bills.objects.get(pk=kwargs["pk"])
        topic_name = request.POST["topic_name"]
        topic_user = request.POST["username"]  # ! BUG HERE
        topic_price = request.POST["topic_price"]
        topic = Topic.objects.create(
            title=topic_name, price=float(topic_price), bill=bill
        )

        user = UserProfile.objects.get(user__username=topic_user)
        topic.add_user(user)

        return HttpResponseRedirect(reverse("bills:add", args=(bill.id,)))
