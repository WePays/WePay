from django.urls import path

from . import views


app_name = "payments"
urlpatterns = [
    # path("", views.bill, name="bill"),
    path("", views.PaymentView.as_view(), name="bill"),
    # path("create/", views.CreateView.as_view(), name="create"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("create/<int:pk>/", views.AddTopicView.as_view(), name="add_topic"),
    # path("<int:bills_id>/add/", views.add_topics, name="add")
    # path("payments/", views.payment, name="payment"),  #! no payments path its a button
    # path("<int:pk>", views.CreateBillView.as_view(), name="create")
    # path("time/", views.showtime, name="time"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # # /polls/5/results/
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # # /polls/5/vote/
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]