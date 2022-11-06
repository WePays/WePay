from django.urls import path

from . import views


app_name = "user-profile"

urlpatterns = [
    path("", views.UserProfileView.as_view(), name="bill"),
]
