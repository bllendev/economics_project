from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from ai.models import Chat
import logging

logger = logging.getLogger(__name__)


class ChatMessagesView(LoginRequiredMixin, View):
    template_name = "partials/chat_messages.html"

    def get(self, request, chat_pk, *args, **kwargs):
        # validate chat_pk
        if not chat_pk:
            raise RuntimeError("Missing context no chat_pk!")

        # get chat
        chat = get_object_or_404(Chat, pk=chat_pk)

        # return rendered chat - we unroll messages in the template
        return render(request, self.template_name, {"chat": chat})
