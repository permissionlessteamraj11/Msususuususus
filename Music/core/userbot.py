from pyrogram import Client
import config

class Assistant(Client):
    def __init__(self):
        super().__init__(
            name="PritiAssistant",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=config.STRING_SESSION,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = f"{get_me.first_name} {get_me.last_name or ''}"
        print(f"Assistant started as {self.name} (@{self.username})")

    async def stop(self):
        await super().stop()
        print("Assistant stopped.")
