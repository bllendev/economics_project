# django
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

# tools
from openai import OpenAI
from decouple import config

# local
from ai.models import Conversation, Message
from ai.constants import TOKEN_USAGE_DAILY_LIMIT, AI_PROMPT


client = OpenAI(api_key=config("OPENAI_API_KEY"))

CustomUser = get_user_model()


@csrf_exempt
def create_conversation(request):
    try:
        # extract user info
        username = request.user.username
        if not username:
            return JsonResponse({})
        user = CustomUser.objects.get(username=username)

        # check if conversation_id exists in the session
        conversation = Conversation.objects.create(user=user)
        system_query = [{"role": "system", "content": AI_PROMPT}]

        # create a message for the system prompt (ai)
        Message.objects.create(
            conversation=conversation,
            sender=Message.SENDER_AI,
            text=AI_PROMPT,
        )

        # return the conversation_id in the response
        return JsonResponse({"conversation_id": conversation.id})

    except Exception as e:
        print(f"create_conversation - ERROR: {e}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)
