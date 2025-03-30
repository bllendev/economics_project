from django.db import models
from common.models import BaseModel


class Message(BaseModel):
    USER_MESSAGE = "User"
    AI_MESSAGE = "AI"
    MESSENGER_CHOICES = (
        (USER_MESSAGE, USER_MESSAGE),
        (AI_MESSAGE, AI_MESSAGE),
    )

    index = models.IntegerField(default=0)
    chat = models.ForeignKey(
        "ai.Chat", on_delete=models.SET_NULL, null=True, related_name="messages"
    )
    messenger = models.CharField(
        max_length=256, choices=MESSENGER_CHOICES, default=USER_MESSAGE
    )
    text = models.TextField(default="", blank=True)

    def save(self, *args, **kwargs):
        # Check if it's an AI response and the last message was from a user
        if self.messenger == self.AI_MESSAGE:
            last_message = self.chat.messages.last()
            if not last_message.messenger == self.USER_MESSAGE:
                raise RuntimeError(
                    "We expected the last message to be from the user..."
                )

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["index"]

    def __str__(self):
        return f"{self.messenger}: {self.text[:50]}..."
