import asyncio
try:
    from pytgcalls import PyTgCalls
    from pytgcalls.types import Update
    from pytgcalls.types import MediaStream, AudioQuality, VideoQuality
    HAS_PYTGCALLS = True
except ImportError:
    PyTgCalls = object
    HAS_PYTGCALLS = False

import config
from Music.core.userbot import Assistant

class Call(PyTgCalls):
    def __init__(self):
        self.userbot = Assistant()
        if HAS_PYTGCALLS:
            super().__init__(self.userbot)

    async def join_call(self, chat_id, audio_url, video=False):
        if not HAS_PYTGCALLS:
            return
        try:
            if video:
                stream = MediaStream(audio_url, audio_parameters=AudioQuality.HIGH, video_parameters=VideoQuality.HD_720P)
            else:
                stream = MediaStream(audio_url, audio_parameters=AudioQuality.HIGH)
            await self.play(chat_id, stream)
        except Exception as e:
            print(f"Error joining call: {e}")

    async def leave_call(self, chat_id):
        if not HAS_PYTGCALLS:
            return
        try:
            await self.leave_group_call(chat_id)
        except Exception as e:
            print(f"Error leaving call: {e}")

    async def pause_stream_call(self, chat_id):
        if not HAS_PYTGCALLS:
            return
        try:
            await self.pause_stream(chat_id)
        except Exception as e:
            print(f"Error pausing call: {e}")

    async def resume_stream_call(self, chat_id):
        if not HAS_PYTGCALLS:
            return
        try:
            await self.resume_stream(chat_id)
        except Exception as e:
            print(f"Error resuming call: {e}")

    async def start(self):
        await self.userbot.start()
        if HAS_PYTGCALLS:
            await super().start()
        print("Voice Call Handler started.")

    async def stop(self):
        if HAS_PYTGCALLS:
            await super().stop()
        await self.userbot.stop()
        print("Voice Call Handler stopped.")

call = Call()

if HAS_PYTGCALLS:
    @call.on_stream_end()
    async def stream_end_handler(_, update: Update):
        from Music.helpers.queue import pop_from_queue

        chat_id = update.chat_id
        next_song = await pop_from_queue(chat_id)
        if next_song:
            await call.join_call(chat_id, next_song["link"], video=next_song["video"])
        else:
            try:
                await call.leave_group_call(chat_id)
            except:
                pass
