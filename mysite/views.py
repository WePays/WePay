from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from auth_remember import remember_user


class Home(TemplateView):
    template_name = "Wepay/index.html"


def signup(request):
    """Register a new user."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_passwd = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
            remember_user(request, user)
            return redirect("WePay/login")
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
