from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from ai.models import Chat, Message
from common.forms import BaseCreateForm

import logging
logger = logging.getLogger(__name__)


class ChatForm(BaseCreateForm):
    class Meta:
        model = Chat
        fields = ['ai']

    def __init__(self, *args, **kwargs):
        self.user_message = kwargs.pop("user_message", None)
        super(ChatForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'ai',
            Submit('submit', 'Save')
        )
    
    def save(self, commit=True):
        logger.debug("ChatForm save...")
        obj = super(ChatForm, self).save(commit=False)
        if commit:
            obj.save() # NOTE: create obj then create message

            # create first user message too (if we pass one upon create of chat)
            if self.user_message:
                logger.debug(f"creating first message for newly created chat {obj}")
                message = Message.objects.create(
                    chat=obj,
                    text=self.user_message,
                    messenger=Message.USER_MESSAGE,
                    index=0,
                )

        return obj


class MessageForm(BaseCreateForm):
    class Meta:
        model = Message
        fields = ['messenger', 'chat', 'text', 'index']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'messenger',
            'chat',
            'text',
            'index',
            Submit('submit', 'Save')
        )
