from django.urls import path

from . import views


app_name = "payments"
urlpatterns = [
    # path("", views.bill, name="bill"),
    path("", views.PaymentView.as_view(), name="bill"),
    # path("create/", views.CreateView.as_view(), name="create"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
]
