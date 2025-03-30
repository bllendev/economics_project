from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger(__name__)


class ChatsView(LoginRequiredMixin, View):
    template_name = "partials/chats.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        chats = user.profile.chats.all()
        return render(request, self.template_name, {"chats": chats})
