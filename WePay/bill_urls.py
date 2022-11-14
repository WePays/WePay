from django.urls import path

from . import views


app_name = "bills"
urlpatterns = [
    # path("", views.bill, name="bill"),
    path("", views.BillView.as_view(), name="bill"),
    path("create/", views.BillCreateView.as_view(), name="create"),
    path("<int:pk>/add", views.AddTopicView.as_view(), name="add"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/add/success", views.create, name="success"),
    path("<int:pk>/add/close", views.close, name="close"),
    path("<int:pk>/delete", views.DetailView.as_view(), name="delete"),

]
