"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings

from .views import About, Instruction, Tailwind, signup

# from django.conf.urls import url


urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("bill/", include("WePay.bill_urls")),
    path("payment/", include("WePay.payment_urls")),
    path("accounts/", include("allauth.urls")),
    path("signup/", signup, name="signup"),
    path("about/", About.as_view(), name="about"),
    path("user-profile/", include("WePay.user_profile_urls")),
    path("history/", include("WePay.history_urls")),
    path("instruction/", Instruction.as_view(), name="instruction"),
    path("topic/", include("WePay.topic_urls")),
    path("", RedirectView.as_view(url="/bill/")),
    path("__reload__/", include("django_browser_reload.urls")),
    path("tailwind/", Tailwind.as_view(), name="tailwind"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
