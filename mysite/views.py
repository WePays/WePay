from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


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
            return redirect("WePay/login")
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


class About(TemplateView):
    """Template view for about us page."""

    template_name = "Wepay/about.html"


class Instruction(TemplateView):
    """Template view for instruction page."""

    template_name = "Wepay/Instruction.html"


class Tailwind(TemplateView):
    """Test page for tailwind"""

    template_name = "Wepay/test_tailwind.html"
