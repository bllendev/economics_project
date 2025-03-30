from common.views import BaseCreateUpdateView
from ai.models import Message
from ai.forms import MessageForm
import logging

logger = logging.getLogger(__name__)


class MessageUpdateView(BaseCreateUpdateView):
    model = Message
    form_class = MessageForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        message = self.get_object()
        if message.messenger == Message.USER_MESSAGE:
            self.form_html_get = "partials/chat_message_user.html"
        elif message.messenger == Message.AI_MESSAGE:
            self.form_html_get = "partials/chat_message_ai.html"

        response = super().get(request, *args, **kwargs)
        return response
