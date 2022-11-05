from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse
from ..models import UploadTopicForm, Bills, Topic, Payment


class AddTopicView(LoginRequiredMixin, generic.DetailView):
    """views for add topic to bills."""

    template_name = "Wepay/add_topic.html"
    model = Bills, Topic

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            bills = Bills.objects.get(pk=pk)
        except Bills.DoesNotExist:
            return HttpResponseRedirect(reverse("bills:bill"))
        return render(
            request,
            "Wepay/add_topic.html",
            {"bills": bills, "form_topic": UploadTopicForm},
        )

    def post(self, request, *args, **kwargs):
        form_topic = UploadTopicForm(request.POST)
        if form_topic.is_valid():
            form_topic.save()
        return HttpResponseRedirect(reverse("bills:bill"))
