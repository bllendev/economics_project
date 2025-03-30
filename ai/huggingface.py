import os
import requests
import logging

logger = logging.getLogger(__name__)

# api token
API_TOKEN = os.getenv('HUGGINGFACE_TOKEN')

# models in use
HUGGINGFACE_API_INTENT_DISTILLED_BERT_0 = os.getenv("HUGGINGFACE_API_INTENT_DISTILLED_BERT_0")


# validate
if not API_TOKEN:
    logger.error("NO HUGGINGFACE TOKEN!!!")
    # raise RuntimeError(f"Missing HUGGINGFACE_TOKEN.... {API_TOKEN}")

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def parse_user_intent(user_input):
    """
    Uses the Hugging Face Inference API to classify user input and predict the intent.
    """
    payload = {"inputs": user_input}

    try:
        response = requests.post(HUGGINGFACE_API_INTENT_DISTILLED_BERT_0, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()

        # Extract the label with the highest score
        max_label = max(result[0], key=lambda x: x['score'])
        predicted_intent = max_label['label']
        
        logger.info(f"The predicted intent is: {predicted_intent}")
        return predicted_intent
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during inference API call: {e}")
        return None
