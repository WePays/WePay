from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.shortcuts import render
from ..models import UploadTopicForm, Bills, Topic


