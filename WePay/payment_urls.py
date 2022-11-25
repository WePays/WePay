from django.urls import path

from . import views


app_name = "payments"

urlpatterns = [
    path("", views.PaymentView.as_view(), name="payment"),
    path("<int:pk>/", views.PaymentDetailView.as_view(), name="detail"),
    path("<int:pk>/update", views.update, name="update"),
    path("<int:pk>/confirm", views.confirm_payment, name="confirm"),
    path("<int:pk>/reset", views.reset, name="reset"),
    path("<int:pk>/reject", views.reject, name="reject"),
    path("<int:pk>/qr", views.QRViews.as_view(), name="qr"),
]
