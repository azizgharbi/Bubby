import asyncio
import sys
from Bot import Bot

prompt = sys.argv[1]
bot = Bot()

reply = bot.make_request(prompt)


async def main():
    await bot.send_msg(reply)


asyncio.run(main())
