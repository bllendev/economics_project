from django.urls import path
from ai import views
from ai import models

app_name = "ai"

urlpatterns = [
    # chats (ai to user messaging)
    path("chats/", views.ChatsView.as_view(), name="chats"),
    path(
        "chat-messages/<uuid:chat_pk>/",
        views.ChatMessagesView.as_view(),
        name="chat-messages",
    ),
]

urlpatterns.extend(models.AI.get_urls())
urlpatterns.extend(models.AISettings.get_urls())
urlpatterns.extend(models.Chat.get_urls())
urlpatterns.extend(models.Message.get_urls())
