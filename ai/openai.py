import json
import logging
from django.conf import settings
from openai import OpenAI

logger = logging.getLogger(__name__)


class OpenAIWrapper:
    def __init__(self, api_key=None):
        logger.info("openai ai wrapper init...")
        self.api_key = api_key or settings.OPENAI_KEY
        self.client = OpenAI(api_key=self.api_key)

    def generate_response(
        self,
        prompt,
        model="gpt-4-turbo-2024-04-09",
        max_tokens=4096,
        temperature=0.7,
        **kwargs,
    ):
        logger.info("generating text...")
        messages = kwargs.pop("messages", [{"role": "user", "content": prompt}])
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs,
        )
        message = response.choices[0].message.content.strip()
        logger.info(f"generated message: {message}")
        return message

    def generate_structured_content(self, raw_content):
        prompt = (
            "You are a sophisticated AI tasked with structuring report content. "
            "Here is a masked report content that needs to be structured meaningfully as per the contents of the report, and turned into valid JSON format. "
            "The structure **may** include sections and contents with the following format:\n"
            "{\n"
            '  "sections": [\n'
            "    {\n"
            '      "name": "Section Name",\n'
            '      "index": 0,\n'
            '      "description": "Description of the section",\n'
            '      "pk": "section-pk",\n'
            '      "contents": [\n'
            "        {\n"
            '          "name": "Content Name",\n'
            '          "index": 0,\n'
            '          "pk": "content-pk",\n'
            '          "description": "Description of the content",\n'
            '          "text": "Content text"\n'
            "        }\n"
            "      ]\n"
            "    }\n"
            "  ]\n"
            "}\n\n"
            "It may be the case only contents are provided without sections, in this case assume to restructure the report including creating new sections such that you can meaningfully structure content to the best of your ability.\n\n"
            "In the json response, be sure the new arrangement of the structure reflects in the datastructure including nesting of sections and contents, naturally describing the report hierarchy.\n\n"
            "Should you create new sections, leave their respective pk fields blank, fill out other necessary information as needed such that the report is structured as seemingly intended.\n\n"
            "Please ensure all property names and string values are enclosed in double quotes:\n\n"
            "If the report you recieved is not in the correct format, return the following message... ERROR: (describe the error or wonky nature of content here...)"
            f"{raw_content}"
        )
        response = self.generate_response(prompt)
        if "ERROR:" in response[:6]:
            raise ValueError(response)
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON response: {e}")
            raise
