from django.urls import path

from . import views


app_name = "user-profile"

urlpatterns = [
    path("", views.UserProfileView.as_view(), name="userprofile"),
    path("fetch-key/", views.fetch_key, name="fetch-key"),
]
