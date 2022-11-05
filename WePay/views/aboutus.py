from django.views import generic


class AboutUsView(generic.TemplateView):
    """views for aboutus.html"""

    template_name = "Wepay/aboutus.html"
