from django.template.loader import render_to_string

import logging

logger = logging.getLogger(__name__)


class NotificationMixin:
    """Mixin for adding notifications to a view
    ... used for adding success or error messages to views
    """

    def __init__(self, *args, **kwargs):
        self.notification = ""

    def get_notification_success(self):
        notification = ""
        if self.notification:
            notification = render_to_string(
                "partials/notification_success.html",
                {"message": self.notification},
                request=self.request,
            )
        return notification
