import os
from pyrogram import Client, errors
import config

class MusicBot(Client):
    def __init__(self):
        super().__init__(
            name="PritiMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            plugins=dict(root="Music.plugins"),
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = get_me.first_name
        print(f"Bot started as {self.name} (@{self.username})")

    async def stop(self):
        await super().stop()
        print("Bot stopped.")
