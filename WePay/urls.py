from django.urls import path

from . import views


app_name = "bills"
urlpatterns = [
    # path("", views.bill, name="bill"),
    path("", views.BillView.as_view(), name="bill"),
    path("create/", views.create, name="create"),
    path("detail/", views.detail, name="detail"),
    path("payments/", views.payment, name="payment"),
    # path("<int:pk>", views.CreateBillView.as_view(), name="create")
    # path("time/", views.showtime, name="time"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # # /polls/5/results/
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # # /polls/5/vote/
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]
