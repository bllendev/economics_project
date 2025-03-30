from common.views import BaseCreateUpdateView
from ai.models import Chat
from ai.forms import ChatForm
import logging

logger = logging.getLogger(__name__)


class ChatUpdateView(BaseCreateUpdateView):
    model = Chat
    form_class = ChatForm
