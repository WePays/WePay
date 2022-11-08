from django.urls import path

from . import views


app_name = "payments"

urlpatterns = [
    path("", views.PaymentView.as_view(), name="payment"),
    path("<int:pk>/", views.PaymentDetailView.as_view(), name="detail"),
]
