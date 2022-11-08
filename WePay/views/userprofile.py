import omise
from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from django.http import HttpResponseRedirect
from django.views.generic import DetailView

from ..models import UserProfile


class UserProfileView(DetailView):
    """Template view for user profile page."""

    template_name = "Wepay/user_profile.html"
    Model = UserProfile

    def get(self, request, *args, **kwargs):
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        chain_key = userprofile.chain_key
        return render(
            request, self.template_name, {"user": user, "chain_key": chain_key}
        )

    def post(self, request, *arg, **kwargs):
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        display_name = request.POST["display name"]
        chain_key = request.POST["chain key"]
        try:
            omise.Chain.retrieve(chain_key)
        except omise.errors.NotFoundError:
            messages.error(request, "Invalid Chain Key")
            return HttpResponseRedirect(reverse("user-profile:userprofile"))
        userprofile.chain_key = chain_key

        user.username = display_name
        user.save()
        userprofile.save()

        return redirect("/")
