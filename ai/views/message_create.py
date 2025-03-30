from django.shortcuts import render
from django.shortcuts import get_object_or_404
from common.views import BaseCreateUpdateView
from ai.models import Chat, Message
from ai.forms import MessageForm
from ai.utils import ChatManager
import logging

logger = logging.getLogger(__name__)


class MessageCreateView(BaseCreateUpdateView):
    model = Message
    form_class = MessageForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_pk = None
        self.messenger = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        data = dict()

        # add chat_pk
        if self.chat_pk:
            self.chat = get_object_or_404(Chat, pk=self.chat_pk)
            last_message = self.chat.messages.last()
            index = 0 if not last_message else last_message.index + 1
            data_chat_pk = {"chat": self.chat, "index": index}
            data.update(data_chat_pk)

        # add messenger
        if self.messenger:
            data_messenger = {"messenger": self.messenger}
            data.update(data_messenger)

        # create ai response if messenger is ai and user is last message (we use as context)
        if self.messenger == Message.AI_MESSAGE:
            last_message = self.chat.messages.last()
            index = 0 if not last_message else last_message.index + 1
            chat_manager = ChatManager(self.chat)
            ai_response = chat_manager.process_user_input(last_message, self.user.id)
            self.text = ai_response

        # add text
        if self.text:
            data_text = {"text": self.text}
            data.update(data_text)

        # update pre-form data init
        if data:
            kwargs.update({"data": data})

        logger.info(f"MessageCreateView get_form_kwargs ... {kwargs} ")
        return kwargs

    def post(self, request, *args, **kwargs):
        # unpack chat_pk, validate
        self.chat_pk = request.POST.get("chat_pk")
        if not self.chat_pk:
            logger.warning(
                "no chat_pk passed upon MessageCreateView - assume to create new Chat as well !"
            )
            # raise RuntimeError("Missing context, no chat!")

        # unpack messenger, validate
        self.messenger = request.POST.get("messenger")
        if not self.messenger:
            raise RuntimeError("Missing context, no  messenger!")

        # unpack text, validate
        self.text = request.POST.get("text")
        if not self.text and self.messenger == Message.USER_MESSAGE:
            raise RuntimeError("Missing context, no text from user!")

        # set message return html (handle state b/t user or ai)
        match self.messenger:
            case Message.USER_MESSAGE:
                self.form_html_post = "partials/chat_message_user.html"

            case Message.AI_MESSAGE:
                self.form_html_post = "partials/chat_message_ai.html"

            case _:
                raise RuntimeError(f"unsupported messenger case... {self.messenger}")

        # validate!
        response = super().post(request, *args, **kwargs)
        # if response.status_code != 200:
        #     raise RuntimeError(f"bad response ... {response}")

        # save okay - return message html partial
        last_message = self.chat.messages.last()
        response = render(request, self.form_html_post, {"message": last_message})

        # trigger ai response (if user sent message)
        if self.messenger == Message.USER_MESSAGE:
            response["HX-Trigger-After-Swap"] = "refresh-forms-chat-message-ai"

        return response
