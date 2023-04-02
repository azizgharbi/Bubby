import telegram
from typing import Any
import openai
from config import TOKEN, CHANNEL_ID, API_KEY
import speech_recognition as sr


class Bot:
    def __init__(self):
        self.messages = []
        self.token = TOKEN
        self.chanel_id = CHANNEL_ID
        self.api_key = API_KEY
        self.bot = telegram.Bot(token=self.token)
        openai.api_key = self.api_key

    def transcribe_wav_file(self, file_path):
        """transcribe audio wav_file"""
        r = sr.Recognizer()
        # open the WAV file
        with sr.AudioFile(file_path) as source:
            # read the audio data from the file
            audio_data = r.record(source)
            # recognize speech using the Google Speech Recognition API
            text = r.recognize_google(audio_data)
            self.messages.append({"role": "user", "content": text})
        # return the transcribed text
        return text

    def make_request(self, prompt) -> str | None:
        """Make a request using open.ai ChatCompletion"""
        try:
            self.messages.append({"role": "user", "content": prompt})

            response: Any = (
                openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=self.messages
                )
                or None
            )

            if response is not None:
                reply = response.get("choices")[0]["message"].content or None
                if reply:
                    return reply
            return response
        except Exception as error:
            print(error)

    async def send_msg(self, msg) -> None:
        """Echo the assistant message."""
        if msg is not None:
            self.messages.append({"role": "user", "content": msg})
            await self.bot.send_message(chat_id=CHANNEL_ID, text=msg)
        else:
            await self.bot.send_message(chat_id=CHANNEL_ID, text="Something wrong!")
