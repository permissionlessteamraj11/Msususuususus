import asyncio
import os
from aiohttp import web

# Fix for "RuntimeError: There is no current event loop in thread 'MainThread'"
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from Music.core.bot import MusicBot
from Music.core.call import call

async def handle(request):
    return web.Response(text="PritiMusic Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server started on port {port}")

async def main():
    await start_web_server()
    bot = MusicBot()
    await bot.start()
    await call.start()
    print("PritiMusic Bot and Assistant are running.")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop.run_until_complete(main())
