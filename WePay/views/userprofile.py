from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views.generic import DetailView

from ..config import OMISE_SECRET
from ..models import UserProfile, omise


class UserProfileView(LoginRequiredMixin, DetailView):
    """Template view for user profile page."""

    template_name = "Wepay/user_profile.html"
    Model = UserProfile

    def get(self, request, *args, **kwargs):
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        chain_id = userprofile.chain_id
        return render(request, self.template_name, {"user": user, "chain_id": chain_id})

    def post(self, request, *arg, **kwargs):
        user = request.user
        display_name = request.POST["display name"]

        user.username = display_name
        user.save()
        messages.success(request, f"* Display name has updated to {display_name}")
        return HttpResponseRedirect(reverse("user-profile:userprofile"))


def fetch_key(request, *args, **kwargs):
    """Fetch chain key from user profile."""
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    omise.api_secret = OMISE_SECRET
    all_chain = omise.Chain.retrieve()
    print(user.email)

    for each_chain in all_chain:
        if each_chain.email == user.email:
            userprofile.chain_id = each_chain.id
            userprofile.save()
            messages.success(request, "Chain key is fetched and found")
            break
    else:
        messages.info(
            request,
            "* No Chain found, make sure you follow this \
                <a href='/instruction'>instructions</a> for appling a chain key",
            extra_tags="safe",
        )

    return HttpResponseRedirect(reverse("user-profile:userprofile"))
