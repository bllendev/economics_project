from common.views import BaseDeleteView
from ai.models import Message

import logging

logger = logging.getLogger(__name__)


class MessageDeleteView(BaseDeleteView):
    model = Message
