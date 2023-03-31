import telegram
from typing import Any
import openai
from config import TOKEN, CHANNEL_ID, API_KEY


class Bot:
    def __init__(self):
        self.messages = []
        self.token = TOKEN
        self.chanel_id = CHANNEL_ID
        self.api_key = API_KEY
        self.bot = telegram.Bot(token=self.token)
        openai.api_key = self.api_key

    def make_request(self, prompt) -> str | None:
        """Make a request using open.ai ChatCompletion"""
        self.messages.append({"role": "user", "content": prompt})

        response: Any = (
            openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
            or None
        )

        if response is not None:
            reply = response.get("choices")[0]["message"].content or None
            if reply:
                return reply
        return response

    async def send_msg(self, msg) -> None:
        """Echo the assistant message."""
        await self.bot.send_message(chat_id=CHANNEL_ID, text=msg)
