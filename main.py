import tempfile
import soundfile as sf
from typing import Any
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from Bot import Bot

# For a description of the Bot API, see this page: https://core.telegram.org/bots/api
# Bot Examples
# https://docs.python-telegram-bot.org/en/stable/examples.html

bot = Bot()


async def handle_audio(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if update.channel_post and update.channel_post.voice:
        file_id: Any = update.channel_post.voice.file_id
        file: Any = await bot.bot.get_file(file_id)
        # download audio data from file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".oga") as temp_file:
            temp_file.write(await file.download_as_bytearray())
            temp_file.flush()
            audio_path = temp_file.name
        # convert audio to wav format
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_file:
            data, samplerate = sf.read(audio_path)
            sf.write(wav_file.name, data, samplerate, subtype="PCM_16")
            wav_path = wav_file.name
        # reply
        text = bot.transcribe_wav_file(wav_path)
        reply = bot.make_request(text)
        await bot.send_msg(reply)


async def echo(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    if update.channel_post:
        reply = bot.make_request(update.channel_post.text)
        # reply
        await bot.send_msg(reply)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot.token).build()
    application.add_handler(MessageHandler(filters.TEXT, echo))
    application.add_handler(MessageHandler(filters.VOICE, handle_audio))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


main()
