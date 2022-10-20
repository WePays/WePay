from django.urls import path

from . import views


app_name = "bills"
urlpatterns = [
    # path("", views.BillView.as_view(), name="bill"),
    # path("time/", views.showtime, name="time"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # # /polls/5/results/
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # # /polls/5/vote/
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]
