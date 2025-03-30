from common.views import BaseDeleteView
from ai.models import Chat
import logging

logger = logging.getLogger(__name__)


class ChatDeleteView(BaseDeleteView):
    model = Chat
