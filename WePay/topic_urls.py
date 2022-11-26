from django.urls import path

from . import views


app_name = "topic"

urlpatterns = [
    path("<int:pk>/delete", views.delete_topic, name="delete"),
]
