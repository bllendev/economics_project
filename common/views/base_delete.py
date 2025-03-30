from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic.edit import DeleteView

from ..views.notification_mixin import NotificationMixin
import logging

logger = logging.getLogger(__name__)


class BaseDeleteView(LoginRequiredMixin, NotificationMixin, DeleteView):
    """
    Base view for deleting an object.
    define the django crispy form in forms.py (inherit from common.forms.BaseDeletionView)
    define the deletion view in your views for your model (inheriting from this)
    define url as the following... '("model-name-id-deletion/", ModelDeletionView.as_view(), name="model-name-id-deletion"),
    """

    def __init__(self, *args, **kwargs):
        self.notification = f"{self.model_name} successfully deleted!"

    @property
    def model_name(self):
        """creates a predicatble lower case model name
        ex. "due diligence report"
        """
        return self.model._meta.verbose_name.lower()

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete method on the fetched object and then redirects to the success URL.
        """
        obj = self.get_object()
        obj.delete()
        # Prepare the message
        message_html = self.get_notification()
        response = HttpResponse(message_html, content_type="text/html")
        response["HX-Trigger"] = "refresh-forms, close-modal"
        response["HX-Trigger-After-Swap"] = "notification-added"
        return response

    def get_context_data(self, **kwargs):
        """
        Insert the single object into the context dict.
        """
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        return context
