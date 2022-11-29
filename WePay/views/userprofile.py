from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render, reverse
from django.views.generic import DetailView
from django.conf import settings
from django.db import IntegrityError
from ..models import UserProfile, omise


class UserProfileView(LoginRequiredMixin, DetailView):
    """Username change handler and fetch key

    **Context**

    ``user``
        :model:`auth.User` current user

    ``chain_id``
        chain id of user to make payer can pay with Omise

    **Template**

    :template:`Wepay/userprofile.html`
    """

    template_name = "Wepay/user_profile.html"
    Model = UserProfile

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        get username and chainkey from user that authenticated
        """
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        chain_id = userprofile.chain_id
        return render(request, self.template_name, {"user": user, "chain_id": chain_id})

    def post(self, request: HttpRequest, *arg, **kwargs) -> HttpResponse:
        user = request.user
        display_name = request.POST["display name"]
        user.username = display_name

        try:
            user.save()
        except IntegrityError:
            messages.error(request, "Username already exists")
            return HttpResponseRedirect(reverse("user-profile:userprofile"))


        messages.success(request, f"* Display name has updated to {display_name}")
        return HttpResponseRedirect(reverse("user-profile:userprofile"))


def fetch_key(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    """Fetch chain key from user profile."""
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    omise.api_secret = settings.OMISE_SECRET
    all_chain = omise.Chain.retrieve()

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
                <font color='blue' text underline><a href='/instruction'>instructions</a></font> for appling a chain key",
            extra_tags="safe",
        )
    return HttpResponseRedirect(reverse("user-profile:userprofile"))
