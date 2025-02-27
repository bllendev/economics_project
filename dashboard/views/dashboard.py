from django.views.generic import TemplateView
import logging

logger = logging.getLogger(__name__)


class DashboardView(TemplateView):
    template_name = "partials/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
