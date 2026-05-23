import asyncio
from Music.core.bot import MusicBot
from Music.core.call import call

async def main():
    bot = MusicBot()
    await bot.start()
    await call.start()
    print("PritiMusic Bot and Assistant are running.")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
