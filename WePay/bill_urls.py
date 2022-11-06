from django.urls import path

from . import views


app_name = "bills"
urlpatterns = [
    # path("", views.bill, name="bill"),
    path("", views.BillView.as_view(), name="bill"),
    path("create/", views.BillCreateView.as_view(), name="create"),
    path("<int:pk>/add/", views.AddTopicView.as_view(), name="add"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # # /polls/5/results/
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # # /polls/5/vote/
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]
