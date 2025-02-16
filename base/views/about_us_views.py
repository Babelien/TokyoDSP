from django.views.generic import TemplateView

class AboutUsView(TemplateView):
    template_name = 'pages/about_us.html'