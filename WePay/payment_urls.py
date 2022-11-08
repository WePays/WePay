from django.urls import path

from . import views


app_name = "payments"

urlpatterns = [
    # path("", views.bill, name="bill"),
    path("", views.PaymentView.as_view(), name="payment"),
    # path("create/", views.CreateView.as_view(), name="create"),
    path("<int:pk>/", views.PaymentDetailView.as_view(), name="detail"),
]
