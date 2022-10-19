# config/views.py
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "Wepay/index.html"
