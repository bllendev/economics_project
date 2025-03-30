from django.shortcuts import render

from common.views import BaseCreateUpdateView
from ai.models import Chat, AI
from ai.forms import ChatForm

import logging

logger = logging.getLogger(__name__)


class ChatCreateView(BaseCreateUpdateView):
    """
    creates a new chat and returns a chat_message.html partial with the newly created chat
    ... and that first message the user submitted to create the new chat
    """

    model = Chat
    form_class = ChatForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_message = None
        self.ai = None
        self.form_html_post = "partials/chat_messages.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        data = dict()

        # add user_message (upon create for new chat)
        logger.debug(f"test ChatCreateView ... {self.user_message}")
        if self.user_message:
            data_user_message = {"user_message": self.user_message}
            kwargs.update(
                data_user_message
            )  # NOTE: placing in kwargs - we handle build in form
            # ... we do this because Message obj does not exist yet, build later in ChatForm

        # add ai
        if self.ai:
            data_ai_message = {"ai": str(self.ai.pk)}
            data.update(data_ai_message)

        # update pre-form
        if data:
            kwargs.update({"data": data})

        logger.info(f"ChatCreateView.get_form_kwargs... {kwargs}")
        return kwargs

    def post(self, request, *args, **kwargs):
        """
        will create first message upon chat create too
        """
        # unpack payload
        self.user_message = request.POST.get("text")
        if not self.user_message:
            raise RuntimeError("missing context - user_message")

        # ai
        self.ai, _ = (
            AI.objects.get_or_create()
        )  # NOTE: just keeping this simple for now until we flesh out how ai's are managed

        # create obj
        response = super().post(request, *args, **kwargs)

        # return nice html we expect to return upon create
        if response.status_code != 200:
            raise RuntimeError(f"bad response ... {response}")

        # render chat_messages
        if not self.get_object():
            raise RuntimeError(f"object error chat create view ... {self.object}")

        response = render(request, self.form_html_post, {"chat": self.object})
        response["HX-Trigger"] = ""
        response["HX-Trigger-After-Swap"] = "refresh-forms-chat-message-ai"
        return response
