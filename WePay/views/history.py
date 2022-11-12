from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import get_object_or_404, render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from ..models import 
from django.db.models import QuerySet


class HistoryView(generic.DetailView):
    pass
