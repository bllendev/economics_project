from django.db import models
from common.models import BaseModel


class Chat(BaseModel):
    ai = models.ForeignKey("ai.AI", on_delete=models.SET_NULL, null=True)
    users = models.ManyToManyField("users.User", related_name="chats", blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.created_by not in self.users.all():
            self.users.add(self.created_by)

    def get_messages(self):
        """
        Prepare a list of all messages in the chat to send to the OpenAI API.
        It transforms the messages into a format suitable for the OpenAI model.
        """
        message_list = []
        for message in self.messages.all().order_by("index"):
            role = "user" if message.messenger == Message.USER_MESSAGE else "assistant"
            message_list.append({"role": role, "content": message.text})

        return message_list
