import telegram
from telegram.ext import Application, ContextTypes, MessageHandler, filters
import openai
from typing import Any

# Config
from config import API_KEY, TOKEN, CHANNEL_ID

# For a description of the Bot API, see this page: https://core.telegram.org/bots/api
# Bot Examples
# https://docs.python-telegram-bot.org/en/stable/examples.html

bot = telegram.Bot(token=TOKEN)
messages = []

openai.api_key = API_KEY


def make_request(prompt) -> str | None:
    """Make a request using open.ai ChatCompletion"""
    messages.append({"role": "user", "content": prompt})

    response: Any = (
        openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages) or None
    )

    if response is not None:
        reply = response.get("choices")[0]["message"].content or None
        if reply:
            return reply

    return response


async def send_msg(msg) -> None:
    """Echo the assistant message."""
    await bot.send_message(chat_id=CHANNEL_ID, text=msg)


async def echo(update: telegram.Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    if update.channel_post:
        reply = make_request(update.channel_post.text)
        if reply is not None:
            messages.append({"role": "assistant", "content": reply})
            await send_msg(reply)
        else:
            await send_msg("Ask again!")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


main()
