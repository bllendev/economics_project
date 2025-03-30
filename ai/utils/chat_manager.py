# ai/chat_manager.py
# from documents.vector.milvus_lite import MilvusWrapper
from ai.openai import OpenAIWrapper
from ai.huggingface import parse_user_intent
from ai.models import Chat

import logging

logger = logging.getLogger(__name__)


class ChatManager:

    def __init__(self, chat: Chat):
        self.chat = chat
        self.llm = OpenAIWrapper()

    def process_user_input(self, message, user_id, report_id=None):
        intent = parse_user_intent(user_input=message.text)
        messages = self.chat.get_messages()
        response = self.llm.generate_response(message.text, messages=messages)
        return response
