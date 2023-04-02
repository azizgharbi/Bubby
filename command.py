import asyncio
import sys
from Bot import Bot


async def main():
    prompt = sys.argv[1]
    bot = Bot()
    reply = bot.make_request(prompt)
    print(reply)
    await bot.send_msg(reply)


asyncio.run(main())
