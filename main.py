from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from Bot import Bot

# For a description of the Bot API, see this page: https://core.telegram.org/bots/api
# Bot Examples
# https://docs.python-telegram-bot.org/en/stable/examples.html

bot = Bot()


async def echo(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    print(bot.messages)
    """Echo the user message."""
    if update.channel_post:
        reply = bot.make_request(update.channel_post.text)
        if reply is not None:
            bot.messages.append({"role": "assistant", "content": reply})
            await bot.send_msg(reply)
        else:
            await bot.send_msg("Ask again!")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot.token).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


main()
